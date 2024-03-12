from motor.motor_asyncio import AsyncIOMotorClient
from model import Asset, PerformanceMetric

MONGO_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "asset_performance"
client = None
database = None

async def connect_to_mongo():
    global client
    global database
    client = AsyncIOMotorClient(MONGO_URL)
    database = client[DATABASE_NAME]
    print("Connected to MongoDB")

async def close_mongo_connection():
    global client
    if client:
        client.close()

# Asset operations
async def insert_asset(asset: Asset):
    asset_document = asset.dict()
    result = await database["assets"].insert_one(asset_document)

    if result.acknowledged:
        return asset
    else:
        raise ValueError("Failed to insert asset")

async def get_asset(asset_id: str):
    asset_document = await database["assets"].find_one({"asset_id": asset_id})
    if asset_document:
        return Asset(**asset_document)
    else:
        return None

async def get_all_assets():
    assets = []
    async for asset_document in database["assets"].find():
        assets.append(Asset(**asset_document))
    return assets

async def update_asset(asset_id: str, asset: Asset):
    asset_document = asset.dict()
    result = await database["assets"].update_one({"asset_id": asset_id}, {"$set": asset_document})
    return asset

async def delete_asset(asset_id: str):
    result = await database["assets"].delete_one({"asset_id": asset_id})
    return result.deleted_count > 0


# Performance metric operations
async def insert_metric(metric: PerformanceMetric):
    metric_document = metric.dict()
    result = await database["performance_metrics"].insert_one(metric_document)

    if result.acknowledged:
        return metric
    else:
        raise ValueError("Failed to insert metric")

async def get_metric(metric_id: str):
    metric_document = await database["performance_metrics"].find_one({"metric_id": metric_id})
    if metric_document:
        return PerformanceMetric(**metric_document)
    else:
        return None

async def get_all_metrics():
    metrics = []
    async for metric_document in database["performance_metrics"].find():
        metrics.append(PerformanceMetric(**metric_document))
    return metrics

async def update_metric(metric_id: str, metric: PerformanceMetric):
    metric_document = metric.dict()
    result = await database["performance_metrics"].update_one({"metric_id": metric_id}, {"$set": metric_document})
    return metric

async def delete_metric(metric_id: str):
    result = await database["performance_metrics"].delete_one({"metric_id": metric_id})
    return result.deleted_count > 0

# Data aggregation functions
async def calculate_average_downtime():
    pipeline = [
        {"$match": {"metric_name": "downtime"}},  # Filter by metric name
        {"$group": {"_id": "$asset_id", "average_downtime": {"$avg": "$value"}}}  # Calculate average downtime per asset
    ]
    cursor = database["performance_metrics"].aggregate(pipeline)
    results = await cursor.to_list(length=None)
    return results

async def calculate_total_maintenance_costs():
    pipeline = [
        {"$match": {"metric_name": "maintenance_costs"}},  # Filter by metric name
        {"$group": {"_id": None, "total_maintenance_costs": {"$sum": "$value"}}}  # Calculate total maintenance costs
    ]
    cursor = database["performance_metrics"].aggregate(pipeline)
    result = await cursor.next()
    return result.get("total_maintenance_costs", 0)

async def identify_assets_with_high_failure_rates(threshold: float = 0.01):
    print(threshold)
    pipeline = [
        {"$match": {"metric_name": "failure_rate", "value": {"$gt": threshold}}},  # Filter by failure rate threshold
        {"$group": {"_id": "$asset_id", "total_failures": {"$sum": 1}}}  # Count total failures per asset
    ]
    cursor = database["performance_metrics"].aggregate(pipeline)
    results = await cursor.to_list(length=None)
    return results
