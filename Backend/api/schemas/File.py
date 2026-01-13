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
    file_name: Optional[str] = None
    bucket_id: Optional[int] = None
    file_content_type: Optional[str] = None
    file_size: Optional[int] = None
    is_public: Optional[bool]=None
    is_deleted: Optional[bool]=None
    created_at: Optional[datetime]=None
    path: Optional[str] = None
    filename: Optional[str] = None
    media_type: Optional[str] = None

    class Config:
        from_attributes = True
