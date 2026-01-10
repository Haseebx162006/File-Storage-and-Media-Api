from Backend.database import Base
from sqlalchemy import Column,Integer, String, DateTime, func, ForeignKey,Boolean,BigInteger
from sqlalchemy.orm import relationship
class Bucket(Base):
    __tablename__="buckets"
    
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    name=Column(String)
    is_public=Column(Boolean,default=True)
    storage_limit=Column(BigInteger)
    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),server_default=func.now())
    used_Storage=Column(BigInteger)
    owner=relationship("User", back_populates="buckets")
    files=relationship("File",back_populates="bucket")