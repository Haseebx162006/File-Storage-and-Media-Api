import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="File Storage API")

# 🔥 CORS — MUST be first thing after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://file-storage-and-media-api.vercel.app",
        "http://localhost:5173"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 🔥 Explicit OPTIONS handler (fixes Vercel preflight bug)
from fastapi import Response

@app.options("/{path:path}")
async def preflight_handler(path: str):
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "https://file-storage-and-media-api.vercel.app",
            "Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# ⬇ Import routers AFTER CORS
from Endpoints.auth_endpoints import auth_endpoints
from Endpoints.bucket_endpoints import bucket_router
from Endpoints.file_endpoints import file_router

app.include_router(auth_endpoints)
app.include_router(bucket_router, prefix="/api")
app.include_router(file_router)

@app.get("/")
def root():
    return {"status": "API running"}
