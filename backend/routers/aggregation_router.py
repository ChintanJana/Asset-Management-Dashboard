from fastapi import APIRouter, HTTPException, Depends
from auth import authenticate_user
from database import calculate_average_downtime, calculate_total_maintenance_costs, identify_assets_with_high_failure_rates
from model import User

aggregation = APIRouter()

# Endpoint to calculate average downtime
@aggregation.get("/average-downtime")
async def get_average_downtime(user: User = Depends(authenticate_user)):
    # Call the data aggregation function to calculate average downtime
    average_downtime = await calculate_average_downtime()
    return {"average_downtime": average_downtime}

# Endpoint to calculate total maintenance costs
@aggregation.get("/total-maintenance-costs")
async def get_total_maintenance_costs(user: User = Depends(authenticate_user)):
    # Call the data aggregation function to calculate total maintenance costs
    total_maintenance_costs = await calculate_total_maintenance_costs()
    return {"total_maintenance_costs": total_maintenance_costs}

# Endpoint to identify assets with high failure rates
@aggregation.get("/assets/high-failure-rates/")
async def get_assets_with_high_failure_rates(threshold: float = 0.01, user: User = Depends(authenticate_user)):
    try:
        assets = await identify_assets_with_high_failure_rates(threshold)
        if not assets:  # Check if the list of assets with high failure rates is empty
            raise HTTPException(status_code=404, detail="No assets with high failure rates found")
        return assets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
