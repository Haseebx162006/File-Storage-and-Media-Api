from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Backend.Auth.config import settings

Base=declarative_base()

engine= create_engine(settings.DATABASE_URL)


session_Local= sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db= session_Local()
    try:
        yield db
    finally:
        db.close()