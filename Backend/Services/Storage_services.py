from Backend.Helpers.storage import StorageManager
from Backend.database import get_db
from Backend.Model.User import User
from Backend.Model.File import File
from Backend.Model.Bucket import Bucket
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from Backend.Schemas.File import File_Response_Schema

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
        4. Save file to disk through StorageManager
        5. Save metadata to DB
        """
        # Get bucket
        bucket = self.db.query(Bucket).filter(Bucket.id == bucket_id).first()
        if not bucket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bucket not found")

        # Check ownership
        if bucket.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this bucket")

        # Check storage quota
        try:
            self.storage_manager.check_storage_quota(file=file, bucket=bucket, db=self.db)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        # Save file to disk
        metadata = self.storage_manager.save_file(
            file_name=file.name,
            content=file.content,
            bucket_id=bucket.id,
            file_content_type=file.content_type
        )

        # Save metadata to DB
        new_file = File(
            name=metadata["file_name"],
            file_size=metadata["file_size"],
            bucket_id=bucket.id,
            md5_hash=metadata["md5_hash"],
            sha256_hash=metadata["sha256_hash"],
            file_path=metadata["file_path"],  # Ensure File model uses file_path
            content_type=metadata["file_content_type"],
            upload_date=metadata["upload_date"]
        )
        self.db.add(new_file)
        self.db.commit()
        self.db.refresh(new_file)

        # Update bucket usage
        bucket.used_Storage += metadata["file_size"]
        self.db.commit()

        return new_file

    def download_file(self, user: User, file_id: int):
        file = self.db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        bucket = self.db.query(Bucket).filter(Bucket.id == file.bucket_id).first()

        if bucket.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot access this bucket")

        content = self.storage_manager.read_file(file.file_path)
        if content is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File not found on storage")

        return File_Response_Schema(
            path=file.file_path,
            filename=file.name,
            media_type=file.content_type,
            id=file.id
        )

    def delete_file(self, user: User, file_id: int):
        file = self.db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

        bucket = self.db.query(Bucket).filter(Bucket.id == file.bucket_id).first()
        if bucket.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot access this bucket")

        success = self.storage_manager.delete_file(file_path=file.file_path)
        if not success:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="File could not be deleted from storage")

        self.db.delete(file)
        self.db.commit()

        # Update bucket usage
        bucket.used_Storage = max(bucket.used_Storage - file.file_size, 0)
        self.db.commit()

        return {"detail": "File deleted successfully"}

    def list_files(self, user: User, bucket_id: int):
        bucket = self.db.query(Bucket).filter(Bucket.id == bucket_id).first()
        if not bucket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bucket not found")

        if bucket.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot access this bucket")

        files = self.db.query(File).filter(File.bucket_id == bucket.id).all()
        return [
            {
                "id": f.id,
                "name": f.name,
                "size": f.file_size,
                "upload_date": f.upload_date,
                "content_type": f.content_type,
                "md5_hash": f.md5_hash
            }
            for f in files
        ]

    def move_file(self, user: User, file_id: int, target_bucket_id: int):
        # Fetch file
        file = self.db.query(File).filter(File.id == file_id).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        # Fetch source and target buckets
        source_bucket = self.db.query(Bucket).filter(Bucket.id == file.bucket_id).first()
        target_bucket = self.db.query(Bucket).filter(Bucket.id == target_bucket_id).first()
        if not source_bucket or not target_bucket:
            raise HTTPException(status_code=404, detail="Bucket not found")

        # Check ownership
        if source_bucket.user_id != user.id or target_bucket.user_id != user.id:
            raise HTTPException(status_code=403, detail="You do not own one of the buckets")

        # Check target quota
        if target_bucket.used_Storage + file.file_size > target_bucket.storage_limit:
            raise HTTPException(status_code=400, detail="Not enough space in target bucket")

        # Move file on disk
        new_bucket_path = self.storage_manager.storage_path / f"bucket_{target_bucket.id}"
        new_file_path = self.storage_manager.file_migrate(
            old_path=file.file_path,
            new_bucket_path=new_bucket_path,
            new_filename=file.name
        )

        # Update DB
        file.bucket_id = target_bucket.id
        file.file_path = new_file_path
        self.db.commit()

        # Update storage usage
        source_bucket.used_Storage = max(source_bucket.used_Storage - file.file_size, 0)
        target_bucket.used_Storage += file.file_size
        self.db.commit()

        return {"detail": f"File '{file.name}' moved to bucket {target_bucket.id}"}
