from Backend.Helpers.storage import StorageManager
from Backend.database import get_db
from Backend.Model.User import User
from Backend.Model.File import File
from Backend.Model.Bucket import Bucket
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

class StorageService:
    def __init__(self, storage_manager: StorageManager, db: Session):
        self.db = db
        self.storage_manager = storage_manager

    def upload_file(self, user: User, bucket_id: int, file: File):
        """
        
        Handles uploading a file to a bucket:
        1. Check bucket exists
        2. Check if user owns bucket
        3. Check storage quota
        4. Save file to disk throughh StorageManager
        5. Save metadata to DB
        
        """
        # Get bucket
        bucket = self.db.query(Bucket).filter(Bucket.id == bucket_id).first()
        if not bucket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bucket not found"
            )

        # Checking if bucket exists
        
        if bucket.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not own this bucket"
            )

        # Checking if Storage is avaliable or not
        try:
            self.storage_manager.check_storage_quota(file=file, bucket=bucket, db=self.db)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

        # 4️ Save file to disk
        metadata = self.storage_manager.save_file(
            file_name=file.name,
            content=file.content,
            bucket_id=bucket.id,
            file_content_type=file.content_type
        )
        
        # Saving datae to DB
        
        new_file = File(
            name=metadata["file_name"],
            file_size=metadata["file_size"],
            bucket_id=bucket.id,
            md5_hash=metadata["md5_hash"],
            sha256_hash=metadata["sha256_hash"],
            path=metadata["file_path"],
            content_type=metadata["file_content_type"],
            upload_date=metadata["upload_date"]
        )
        self.db.add(new_file)
        self.db.commit()
        self.db.refresh(new_file)
        
        bucket.used_Storage = bucket.used_storage + metadata["file_size"]
        self.db.commit()

        return new_file
