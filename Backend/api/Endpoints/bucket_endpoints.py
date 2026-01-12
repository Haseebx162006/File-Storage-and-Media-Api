from fastapi import APIRouter,HTTPException,status
from schemas.Bucket import Bucket_create_Schema, Bucket_Response_schema, Bucket_update_Schema
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db
from Auth.token import get_current_user
from model.User import User
from Services.bucket_service import BucketService
bucket_router=APIRouter(
    prefix="/api/buckets"
)

# Create
@bucket_router.post("",response_model=Bucket_Response_schema)
def create_bucket(bucket:Bucket_create_Schema, db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    bucketservice= BucketService(db=db)
    return bucketservice.create_bucket(user=user,name=bucket.name,storage_limit=bucket.storage_limit)



# Get All
@bucket_router.get("",
    response_model=list[Bucket_Response_schema])
def list_buckets(user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    service = BucketService(db=db)
    return service.list_buckets(user=user)


# GEt by ID
@bucket_router.get(
    "/{bucket_id}",
    response_model=Bucket_Response_schema
)
def get_bucket(
    bucket_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = BucketService(db=db)
    return service.get_bucket(user=user, bucket_id=bucket_id)


# Delete
@bucket_router.delete(
    "/{bucket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_bucket(
    bucket_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = BucketService(db=db)
    service.delete_bucket(user=user, bucket_id=bucket_id)





# Update
@bucket_router.patch(
    "/{bucket_id}",
    response_model=Bucket_Response_schema
)
def update_bucket(
    bucket_id: int,
    data: Bucket_update_Schema,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    service = BucketService(db=db)
    return service.update_bucket(
        user=user,
        bucket_id=bucket_id,
        data=data
    )