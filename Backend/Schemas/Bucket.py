from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Bucket_create_Schema(BaseModel):
    name:str
    is_public:Optional[bool]=True
    storage_limit:Optional[int]=None
    
    
class Bucket_Response_schema(BaseModel):
    id:int
    name:str
    user_id:int
    is_public: bool
    storage_limit: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode=True
        
