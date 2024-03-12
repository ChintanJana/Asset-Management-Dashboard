from fastapi import APIRouter, HTTPException, Depends
from auth import authenticate_user
from database import insert_asset, get_asset, update_asset, delete_asset, get_all_assets
from model import Asset, User

asset = APIRouter()

# Endpoint to create a new asset
@asset.post("/assets/", response_model=Asset)
async def create_asset(asset: Asset, user: User = Depends(authenticate_user)):
    return await insert_asset(asset)

# Endpoint to retrieve all assets
@asset.get("/assets", response_model=list[Asset])
async def get_all_assets_route(user: User = Depends(authenticate_user)):
    try:
        assets = await get_all_assets()
        if not assets:  # Check if the list of assets is empty
            raise HTTPException(status_code=404, detail="No assets found")
        return assets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint to get asset by ID
@asset.get("/assets/{asset_id}", response_model=Asset)
async def read_asset(asset_id: str, user: User = Depends(authenticate_user)):
    asset = await get_asset(asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

# Endpoint to update an asset
@asset.put("/assets/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str, asset: Asset, user: User = Depends(authenticate_user)):
    existing_asset = await get_asset(asset_id)
    if existing_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return await update_asset(asset_id, asset)

# Endpoint to delete an asset
@asset.delete("/assets/{asset_id}")
async def delete_asset_endpoint(asset_id: str, user: User = Depends(authenticate_user)):
    existing_asset = await get_asset(asset_id)
    if existing_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    await delete_asset(asset_id)
    return {"message": "Asset deleted successfully"}
