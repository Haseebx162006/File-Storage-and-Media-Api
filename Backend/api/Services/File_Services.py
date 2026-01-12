from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session
from Helpers.storage import get_storage_manager
from model.User import User
from model.Bucket import Bucket
from model.File import File
from api.database import get_db
from Services.File_Services import StorageService


def upload_file_Service(user: User, bucket_id: int, file: UploadFile, db: Session = Depends(get_db)):
    storage_service = StorageService(db=db)
    content = file.file.read()
    file_data = {
        "name": file.filename,
        "content": content,
        "content_type": file.content_type,
        "file_size": len(content)
    }
    
    result = storage_service.upload_file(user=user, bucket_id=bucket_id, file=file_data)
    
    return result


def delete_file_service(user: User, file_id: int, db: Session = Depends(get_db)):
    storage_service = StorageService(db=db)
    return storage_service.delete_file(user=user, file_id=file_id)


def download_file_service(user: User, file_id: int, db: Session = Depends(get_db)):
    storage_service = StorageService(db=db)
    return storage_service.download_file(user=user, file_id=file_id)


def move_file_service(user: User, file_id: int, target_bucket_id: int, db: Session = Depends(get_db)):
    storage_service = StorageService(db=db)
    return storage_service.move_file(user=user, file_id=file_id, target_bucket_id=target_bucket_id)


def list_files_service(user: User, bucket_id: int, db: Session = Depends(get_db)):
    storage_service = StorageService(db=db)
    return storage_service.list_files(user=user, bucket_id=bucket_id)