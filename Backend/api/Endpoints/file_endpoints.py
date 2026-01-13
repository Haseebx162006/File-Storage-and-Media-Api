from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from model.User import User
from model.Bucket import Bucket
from model.File import File as FileModel
from database import get_db
from Auth.token import get_current_user
import traceback
import io

file_router = APIRouter(prefix="/api")

MAX_FILE_SIZE = 4 * 1024 * 1024  # 4MB for Vercel serverless

# ----------------------------
# Upload file to a bucket
# ----------------------------
@file_router.post("/buckets/{bucket_id}/files", status_code=status.HTTP_201_CREATED)
async def upload_file(
    bucket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        # Validate bucket exists
        bucket = db.query(Bucket).filter(Bucket.id == bucket_id).first()
        if not bucket:
            raise HTTPException(status_code=404, detail=f"Bucket {bucket_id} not found")
        
        # Check ownership
        if bucket.user_id != user.id:
            raise HTTPException(status_code=403, detail="Access denied to this bucket")
        
        # Read file content
        content = await file.read()
        
        # Validate size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File too large. Max size: 4MB")
        
        # Save using storage service
        from Services.Storage_services import StorageService
        storage = StorageService(db=db)
        
        file_data = {
            "name": file.filename,
            "content": content,
            "content_type": file.content_type,
            "file_size": len(content)
        }
        
        result = storage.upload_file(user=user, bucket_id=bucket_id, file=file_data)
        
        return {
            "id": result.id,
            "file_name": result.file_name,
            "file_size": result.file_size,
            "bucket_id": result.bucket_id,
            "created_at": result.created_at.isoformat() if result.created_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR uploading file: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# ----------------------------
# List files in a bucket
# ----------------------------
@file_router.get("/buckets/{bucket_id}/files")
def list_files(bucket_id: int,
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    from Services.Storage_services import list_files_service
    return list_files_service(user=user, bucket_id=bucket_id, db=db)


# ----------------------------
# Download a file
# ----------------------------
@file_router.get("/files/{file_id}/download")
def download_file(file_id: int,
                  user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    # Get file from database
    file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check bucket ownership
    bucket = db.query(Bucket).filter(Bucket.id == file.bucket_id).first()
    if bucket.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Read file from Vercel Blob
    from Helpers.cloud_storage import get_cloud_storage_manager
    storage = get_cloud_storage_manager()
    content = storage.read_file(file.file_path)
    
    # Stream the file
    return StreamingResponse(
        io.BytesIO(content),
        media_type=file.file_content_type,
        headers={"Content-Disposition": f"attachment; filename={file.file_name}"}
    )


# ----------------------------
# Delete a file
# ----------------------------
@file_router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: int,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    from Services.Storage_services import delete_file_service
    delete_file_service(user=user, file_id=file_id, db=db)
    return {"detail": "File deleted successfully"}


# ----------------------------
# Move file between buckets
# ----------------------------
@file_router.patch("/files/{file_id}/move/{target_bucket_id}")
def move_file(file_id: int, target_bucket_id: int,
              user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    from Services.Storage_services import move_file_service
    return move_file_service(user=user, file_id=file_id, target_bucket_id=target_bucket_id, db=db)