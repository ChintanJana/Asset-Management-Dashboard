from pydantic import BaseModel
from bson import ObjectId

class Asset(BaseModel):
    asset_id: str
    asset_name: str
    asset_type: str
    location: str
    purchase_date: str
    initial_cost: float
    operational_status: str

class PerformanceMetric(BaseModel):
    metric_id: str
    asset_id: str
    metric_name: str
    value: float

class User(BaseModel):
    username: str
    password: str
