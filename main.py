
from fastapi import FastAPI
from Backend.database import Base, engine
from Backend.Endpoints.file_endpoints import file_router
from Backend.Endpoints.auth_endpoints import auth_endpoints
from Backend.Endpoints.bucket_endpoints import bucket_router
app=FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_endpoints)
app.include_router(bucket_router)
app.include_router(file_router)