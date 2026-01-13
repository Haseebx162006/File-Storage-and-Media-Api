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
        "https://file-storage-and-media-api.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Explicit OPTIONS handler (fixes Vercel preflight bug)
@app.options("/{path:path}")
async def preflight_handler(path: str):
    return {}

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
