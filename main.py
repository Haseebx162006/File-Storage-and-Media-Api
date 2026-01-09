from fastapi import FastAPI
from Backend.database import Base, engine
from Backend.Endpoints.auth_endpoints import auth_endpoints

app=FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_endpoints)