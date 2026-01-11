from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from Backend.Model.User import User
from Backend.database import get_db
from Backend.Auth.token import get_current_user
from Backend.Services.File_Services import (
    upload_file_Service,
    delete_file_service,
    download_file_service,
    move_file_service,
    list_files_service
)

file_router = APIRouter(prefix="/api")

# ----------------------------
# Upload file to a bucket
# ----------------------------
@file_router.post("/buckets/{bucket_id}/files", status_code=status.HTTP_201_CREATED)
def upload_file(bucket_id: int, file: UploadFile = UploadFile(...),
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return upload_file_Service(user=user, bucket_id=bucket_id, file=file, db=db)


# ----------------------------
# List files in a bucket
# ----------------------------
@file_router.get("/buckets/{bucket_id}/files")
def list_files(bucket_id: int,
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    return list_files_service(user=user, bucket_id=bucket_id, db=db)


# ----------------------------
# Download a file
# ----------------------------
@file_router.get("/files/{file_id}/download")
def download_file(file_id: int,
                  user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    result = download_file_service(user=user, file_id=file_id, db=db)
    
    # The service should return a dict with path and filename
    return FileResponse(path=result.path, filename=result.filename, media_type=result.media_type)


# ----------------------------
# Delete a file
# ----------------------------
@file_router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: int,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    delete_file_service(user=user, file_id=file_id, db=db)
    return {"detail": "File deleted successfully"}


# ----------------------------
# Move file between buckets
# ----------------------------
@file_router.patch("/files/{file_id}/move/{target_bucket_id}")
def move_file(file_id: int, target_bucket_id: int,
              user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    return move_file_service(user=user, file_id=file_id, target_bucket_id=target_bucket_id, db=db)
