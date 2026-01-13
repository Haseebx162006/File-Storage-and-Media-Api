from api.database import Base
from sqlalchemy import Column,Integer, String, DateTime, func,ForeignKey,Boolean,BigInteger
from sqlalchemy.orm import relationship

class File(Base):
    
    __tablename__="files"
    id=Column(Integer,primary_key=True, index=True)
    file_name=Column(String,nullable=False)
    bucket_id=Column(Integer,ForeignKey("buckets.id"),nullable=False)
    file_content_type=Column(String)
    file_size=Column(BigInteger)
    is_public=Column(Boolean,default=True)
    is_deleted=Column(Boolean,default=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String, nullable=False)
    file_url = Column(String, nullable=True)  # Cloud storage URL
    
    bucket=relationship("Bucket",back_populates="files")
    
    