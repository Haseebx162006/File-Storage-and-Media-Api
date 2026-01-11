from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from Backend.Model.Bucket import Bucket
from Backend.Model.File import File
from Backend.Model.User import User

class BucketService:

    def __init__(self, db: Session):
        self.db = db

    #  Creating bucket
    def create_bucket(self, user: User, name: str, storage_limit: int):
        if storage_limit <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Storage limit must be greater than 0"
            )

        # Check duplicate bucket name for user
        existing = (
            self.db.query(Bucket)
            .filter(Bucket.user_id == user.id, Bucket.name == name)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bucket with this name already exists"
            )

        bucket = Bucket(
            name=name,
            user_id=user.id,
            storage_limit=storage_limit,
            used_Storage=0
        )

        self.db.add(bucket)
        self.db.commit()
        self.db.refresh(bucket)

        return bucket

    #  List buckets
    def list_buckets(self, user: User):
        return (
            self.db.query(Bucket)
            .filter(Bucket.user_id == user.id)
            .all()
        )

    #  Get single bucket
    def get_bucket(self, user: User, bucket_id: int):
        bucket = (
            self.db.query(Bucket)
            .filter(Bucket.id == bucket_id)
            .first()
        )

        if not bucket:
            raise HTTPException(status_code=404, detail="Bucket not found")

        if bucket.user_id != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        return bucket

    #  Delete bucket
    def delete_bucket(self, user: User, bucket_id: int):
        bucket = self.get_bucket(user, bucket_id)

        # Check if bucket is empty
        file_count = (
            self.db.query(File)
            .filter(File.bucket_id == bucket.id)
            .count()
        )

        if file_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bucket is not empty"
            )

        self.db.delete(bucket)
        self.db.commit()

        return {"detail": "Bucket deleted successfully"}

    #  Update bucket
    def update_bucket(
        self,
        user: User,
        bucket_id: int,
        name: str | None = None,
        storage_limit: int | None = None
    ):
        bucket = self.get_bucket(user, bucket_id)

        if name:
            bucket.name = name

        if storage_limit is not None:
            if storage_limit < bucket.used_Storage:
                raise HTTPException(
                    status_code=400,
                    detail="New storage limit is less than used storage"
                )
            bucket.storage_limit = storage_limit

        self.db.commit()
        self.db.refresh(bucket)

        return bucket
