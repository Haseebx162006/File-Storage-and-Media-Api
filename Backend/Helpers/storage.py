from pathlib import Path
import hashlib
import uuid
import shutil
from typing import List, Dict
from datetime import datetime
from Backend.Model.File import File
from Backend.Model.Bucket import Bucket
from sqlalchemy import func
from sqlalchemy.orm import Session
class StorageManager:

    def __init__(
        self,
        storage_path: str = "./.storage",
        max_file_size: int = 100 * 1024 * 1024,
        allowed_extensions: List[str] = None
    ):
        self.storage_path = Path(storage_path)
        self.max_file_size = max_file_size

        self.allowed_extensions = allowed_extensions or [
            "pdf", "doc", "docx", "txt", "xlsx", "csv",
            "jpg", "jpeg", "png", "gif", "mp4", "avi"
        ]

        self._ensure_storage_dir()

    # CORE HELPERS``

    def _ensure_storage_dir(self):
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _sanitize_filename(self, filename: str) -> str:
        return filename.replace("..", "").replace("/", "").replace("\\", "")

    def _validate_file_size(self, size: int):
        if size > self.max_file_size:
            raise ValueError("File size exceeded the limit")

    def _validate_extension(self, filename: str) -> str:
        extension = filename.split(".")[-1].lower()
        if extension not in self.allowed_extensions:
            raise ValueError("File type not allowed")
        return extension

    def _generate_file_id(self) -> str:
        return str(uuid.uuid4())

    def _get_bucket_dir(self, bucket_id: int) -> Path:
        bucket_dir = self.storage_path / f"bucket_{bucket_id}"
        bucket_dir.mkdir(parents=True, exist_ok=True)
        return bucket_dir

    def _calculate_hashes(self, content: bytes) -> Dict[str, str]:
        return {
            "md5": hashlib.md5(content).hexdigest(),
            "sha256": hashlib.sha256(content).hexdigest()
        }

    # MAIN FUNCTION

    def save_file(
        self,
        file_name: str,
        content: bytes,
        bucket_id: int,
        file_content_type: str
    ) -> Dict:

        file_name = self._sanitize_filename(file_name)
        file_size = len(content)

        self._validate_file_size(file_size)
        extension = self._validate_extension(file_name)

        file_id = self._generate_file_id()
        bucket_dir = self._get_bucket_dir(bucket_id)

        stored_filename = f"{file_id}.{extension}"
        file_path = bucket_dir / stored_filename

        # Save file
        with open(file_path, "wb") as f:
            f.write(content)

        hashes = self._calculate_hashes(content)
        upload_date = datetime.utcnow()

        return {
            "file_id": file_id,
            "original_name": file_name,
            "bucket_id": bucket_id,
            "stored_name": stored_filename,
            "file_size": file_size,
            "content_type": file_content_type,
            "file_path": str(file_path),
            "md5_hash": hashes["md5"],
            "sha256_hash": hashes["sha256"],
            "uploaded_at": upload_date.isoformat()
        }

    # FILE ACCESS

    def read_file(self, file_path: str) -> bytes:
        path=Path(file_path)
        if not path.exists():
            raise FileNotFoundError("File not found")
        
        return path.read_bytes()

    def delete_file(self, file_path: str) -> bool:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False

    def file_exists(self, file_path: str) -> bool:
        return Path(file_path).exists()
    
    def get_current_used_storage(self, bucket_id: int, db: Session) -> int:
        total = db.query(func.sum(File.file_size))\
              .filter(File.bucket_id == bucket_id)\
              .scalar()
              
        
        return total or 0
              
            

    
    def check_storage_Quota(self, file: dict, bucket: Bucket, db: Session):
         current_used = self.get_current_used_storage(bucket_id=bucket.id, db=db)
    
         # Calculate total after upload
         total_after_upload = current_used + file["file_size"]
    
         if total_after_upload > bucket.storage_limit:
             raise ValueError(f"Low storage: Bucket limit {bucket.storage_limit} bytes, "
                         f"currently used {current_used} bytes, "
                         f"file size {file['file_size']} bytes")
                
    
    
         return {
        "bucket_id": bucket.id,
        "current_used": current_used,
        "file_size": file["file_size"],
        "total_after_upload": total_after_upload,
        "storage_limit": bucket.storage_limit,
        "within_quota": True
         }
         
    def file_migrate(self,old_path:str, new_path:str, new_filename:str )->str:
        new_bucket_path=Path(new_path)
        new_bucket_path.mkdir(parents=True, exist_ok=True)
        
        new_path_2= new_bucket_path/new_filename
        shutil.move(old_path,new_path_2)
        return str(new_path_2)
        
             
            
    

storageManager=StorageManager()