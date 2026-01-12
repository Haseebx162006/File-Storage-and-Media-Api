import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

Base = declarative_base()

# Create engine for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections every hour
)

session_Local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = session_Local()
    try:
        yield db
    finally:
        db.close()