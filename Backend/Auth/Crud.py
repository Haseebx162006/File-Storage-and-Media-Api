
from sqlalchemy.orm import Session
from Backend.Model.User import User
from fastapi import HTTPException,status
from Backend.Schemas.User import Create_User_Schema, Read_User_Schema, Update_User_Schama
from Backend.Auth.Security import hash_password

def search_with_email(email:str,db:Session):
    return db.query(User).filter(User.email==email).first()


def create_user(email:str, password:str, name:str, db:Session):
    if search_with_email(email=email,db=db):
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail="User already exists")
    
    user_hash_password=hash_password(password)
    user=User(
        name=name,
        email=email,
        password=user_hash_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def delete_user(id: int , db:Session):
    user= db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found ")
    
    
    db.delete(user)
    db.commit()
    db.refresh(user)
    
    
    return {"Deletion is completed!"}
        
    