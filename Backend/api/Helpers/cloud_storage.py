import os
from typing import Dict, Optional
from pathlib import Path
import hashlib
import uuid
from datetime import datetime
import requests

class CloudStorageManager:
    """
    Cloud storage manager using Vercel Blob REST API.
    Falls back to local storage for development.
    """
    
    def __init__(self):
        self.blob_token = os.getenv("BLOB_READ_WRITE_TOKEN")
        self.is_production = bool(self.blob_token)
        
        # Fallback to local storage in development
        if not self.is_production:
            self.local_storage_path = Path("./.storage")
            self.local_storage_path.mkdir(parents=True, exist_ok=True)
    
    def save_file(
        self,
        file_name: str,
        content: bytes,
        bucket_id: int,
        file_content_type: str
    ) -> Dict:
        """
        Save file to cloud storage (production) or local (development)
        """
        file_id = str(uuid.uuid4())
        extension = file_name.split(".")[-1].lower() if "." in file_name else "bin"
        stored_filename = f"{file_id}.{extension}"
        
        # Generate blob path
        blob_path = f"bucket_{bucket_id}/{stored_filename}"
        
        if self.is_production:
            # Upload to Vercel Blob via REST API
            try:
                response = requests.put(
                    f"https://blob.vercel-storage.com/{blob_path}",
                    headers={
                        "Authorization": f"Bearer {self.blob_token}",
                        "Content-Type": file_content_type,
                        "x-vercel-blob-add-random-suffix": "0"
                    },
                    data=content
                )
                response.raise_for_status()
                result = response.json()
                file_url = result.get("url", f"https://blob.vercel-storage.com/{blob_path}")
                file_path = file_url  # Store the full URL
            except Exception as e:
                print(f"Blob upload failed: {e}")
                raise
        
        if not self.is_production:
            # Save locally for development
            bucket_dir = self.local_storage_path / f"bucket_{bucket_id}"
            bucket_dir.mkdir(parents=True, exist_ok=True)
            file_path = bucket_dir / stored_filename
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            file_url = f"http://localhost:8000/files/{bucket_id}/{stored_filename}"
            file_path = str(file_path)
        
        # Calculate hashes
        hashes = {
            "md5": hashlib.md5(content).hexdigest(),
            "sha256": hashlib.sha256(content).hexdigest()
        }
        
        return {
            "file_id": file_id,
            "original_name": file_name,
            "bucket_id": bucket_id,
            "stored_name": stored_filename,
            "file_size": len(content),
            "content_type": file_content_type,
            "file_path": file_path,
            "file_url": file_url,
            "md5_hash": hashes["md5"],
            "sha256_hash": hashes["sha256"],
            "uploaded_at": datetime.utcnow().isoformat()
        }
    
    def read_file(self, file_path: str) -> bytes:
        """
        Read file from cloud or local storage
        """
        if self.is_production:
            # For Vercel Blob, file_path should be a URL
            if file_path.startswith("http"):
                response = requests.get(file_path)
                response.raise_for_status()
                return response.content
            else:
                # If it's just a path, construct the full URL
                url = f"https://blob.vercel-storage.com/{file_path}"
                response = requests.get(url, headers={"Authorization": f"Bearer {self.blob_token}"})
                response.raise_for_status()
                return response.content
        else:
            # Read from local storage
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            return path.read_bytes()
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from cloud or local storage
        """
        if self.is_production:
            try:
                # Extract blob path from URL if needed
                if file_path.startswith("http"):
                    # Parse URL to get the path
                    blob_path = file_path.replace("https://blob.vercel-storage.com/", "")
                else:
                    blob_path = file_path
                
                response = requests.delete(
                    f"https://blob.vercel-storage.com/{blob_path}",
                    headers={"Authorization": f"Bearer {self.blob_token}"}
                )
                return response.status_code in [200, 204]
            except Exception as e:
                print(f"Error deleting from Blob: {e}")
                return False
        else:
            path = Path(file_path)
            if path.exists():
                try:
                    path.unlink()
                    return True
                except Exception:
                    return False
            return False
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists
        """
        if self.is_production:
            try:
                # Extract blob path from URL if needed
                if file_path.startswith("http"):
                    blob_path = file_path.replace("https://blob.vercel-storage.com/", "")
                else:
                    blob_path = file_path
                
                response = requests.head(
                    f"https://blob.vercel-storage.com/{blob_path}",
                    headers={"Authorization": f"Bearer {self.blob_token}"}
                )
                return response.status_code == 200
            except:
                return False
        else:
            return Path(file_path).exists()
    
    def move_file(self, old_path: str, new_bucket_id: int, filename: str) -> str:
        """
        Move file between buckets
        """
        new_blob_path = f"bucket_{new_bucket_id}/{filename}"
        
        if self.is_production:
            # Read from old location
            content = self.read_file(old_path)
            
            # Upload to new location
            response = requests.put(
                f"https://blob.vercel-storage.com/{new_blob_path}",
                headers={"Authorization": f"Bearer {self.blob_token}"},
                data=content
            )
            response.raise_for_status()
            result = response.json()
            new_file_url = result.get("url", f"https://blob.vercel-storage.com/{new_blob_path}")
            
            # Delete old file
            self.delete_file(old_path)
            
            return new_file_url
        else:
            # Local file move
            import shutil
            new_bucket_path = self.local_storage_path / f"bucket_{new_bucket_id}"
            new_bucket_path.mkdir(parents=True, exist_ok=True)
            new_file_path = new_bucket_path / filename
            shutil.move(old_path, new_file_path)
            return str(new_file_path)
    
    def get_current_used_storage(self, bucket_id: int, db) -> int:
        """Get current storage usage for a bucket"""
        from model.File import File
        from sqlalchemy import func
        
        total = db.query(func.sum(File.file_size))\
              .filter(File.bucket_id == bucket_id)\
              .scalar()
        return total or 0
    
    def check_storage_Quota(self, file: dict, bucket, db):
        """Check if file upload would exceed bucket quota"""
        current_used = self.get_current_used_storage(bucket_id=bucket.id, db=db)
        total_after_upload = current_used + file["file_size"]
        
        if bucket.storage_limit and total_after_upload > bucket.storage_limit:
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

# Singleton instance
_cloud_storage_manager = None

def get_cloud_storage_manager() -> CloudStorageManager:
    global _cloud_storage_manager
    if _cloud_storage_manager is None:
        _cloud_storage_manager = CloudStorageManager()
    return _cloud_storage_manager