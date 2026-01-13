import sys
import os

# Add the api folder to Python path so imports work on Vercel
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Now import your modules
from Endpoints.file_endpoints import file_router
from Endpoints.auth_endpoints import auth_endpoints
from Endpoints.bucket_endpoints import bucket_router
from database import Base, engine

# Initialize FastAPI app
app = FastAPI(title="File Storage API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://file-storage-and-media-api.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(auth_endpoints)
app.include_router(bucket_router)
app.include_router(file_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the file storage API"}