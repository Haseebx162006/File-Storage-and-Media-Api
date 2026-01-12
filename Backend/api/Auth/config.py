import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL:str=os.getenv("DATABASE_URL")
    SECRET_KEY:str=os.getenv("SECRET_KEY")
    ALGORITHM:str=os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES:str=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS:str=os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    
settings=Config()
