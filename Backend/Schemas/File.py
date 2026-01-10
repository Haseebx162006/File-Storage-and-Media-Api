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
    file_name: str
    bucket_id: int
    file_content_type: Optional[str]
    is_public: bool
    is_deleted: bool
    created_at: datetime

    class Config:
        orm_mode = True
