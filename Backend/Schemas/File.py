from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class File_Create_Schema(BaseModel):
    file_name: str
    bucket_id: int
    file_content_type: Optional[str] = None
    is_public: Optional[bool] = True

class File_Response_Schema(BaseModel):
    id: int
    file_name: Optional[str]
    bucket_id: Optional[int]
    file_content_type: Optional[str]
    file_size= Optional[int]
    is_public: Optional[bool]
    is_deleted: Optional[bool]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
