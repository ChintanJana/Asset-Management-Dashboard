from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import connect_to_mongo, close_mongo_connection
from routers import asset, metric, aggregation
from auth import authenticate_user

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(asset)
app.include_router(metric)
app.include_router(aggregation)

@app.get("/")
async def root(username: str = Depends(authenticate_user)):
    return {"message": f"Hello, {username}"}

# Connect to MongoDB on startup and close connection on shutdown
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
