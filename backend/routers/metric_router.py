from fastapi import APIRouter, HTTPException, Depends
from auth import authenticate_user
from database import insert_metric, get_metric, update_metric, delete_metric, get_all_metrics
from model import PerformanceMetric, User

metric = APIRouter()

# Endpoint to create a new performance metric
@metric.post("/metrics/", response_model=PerformanceMetric)
async def create_metric(metric: PerformanceMetric, user: User = Depends(authenticate_user)):
    return await insert_metric(metric)

# Endpoint to retrieve all metrics
@metric.get("/metrics", response_model=list[PerformanceMetric])
async def get_all_metrics_route(user: User = Depends(authenticate_user)):
    try:
        metrics = await get_all_metrics()
        if not metrics:  # Check if the list of metrics is empty
            raise HTTPException(status_code=404, detail="No metrics found")
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to get performance metric by ID
@metric.get("/metrics/{metric_id}", response_model=PerformanceMetric)
async def read_metric(metric_id: str, user: User = Depends(authenticate_user)):
    metric = await get_metric(metric_id)
    if metric is None:
        raise HTTPException(status_code=404, detail="Performance metric not found")
    return metric

# Endpoint to update a performance metric
@metric.put("/metrics/{metric_id}", response_model=PerformanceMetric)
async def update_metric(metric_id: str, metric: PerformanceMetric, user: User = Depends(authenticate_user)):
    existing_metric = await get_metric(metric_id)
    if existing_metric is None:
        raise HTTPException(status_code=404, detail="Performance metric not found")
    return await update_metric(metric_id, metric)

# Endpoint to delete a performance metric
@metric.delete("/metrics/{metric_id}")
async def delete_metric_endpoint(metric_id: str, user: User = Depends(authenticate_user)):
    existing_metric = await get_metric(metric_id)
    if existing_metric is None:
        raise HTTPException(status_code=404, detail="Performance metric not found")
    await delete_metric(metric_id)
    return {"message": "Performance metric deleted successfully"}
