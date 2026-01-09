from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.Auth.Crud import create_user,delete_user,search_with_email
from Backend.Schemas.User import Create_User_Schema,Update_User_Schama,Read_User_Schema, TokenResponse
from Backend.Auth.Security import verify_password
from Backend.Model.User import User
from fastapi.security import OAuth2PasswordRequestForm
from Backend.Auth.token import create_token
from Backend.Auth.config import settings
from datetime import timedelta
from jose import jwt, JWTError
from Backend.Auth.config import settings

auth_endpoints= APIRouter(prefix="/api")


@auth_endpoints.post("/signup")
def Signup(user: Create_User_Schema, db:Session=Depends(get_db)):
    User=create_user(email=user.email,password=user.password,name=user.name, db=db)
    return user


@auth_endpoints.post("/login",response_model=TokenResponse)
def login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user= search_with_email(form_data.username,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    if not verify_password(form_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    access_token=create_token(data={"sub":str(user.id)},expire_minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token=create_token(data={"sub":str(user.id)},expire_minutes=int(settings.REFRESH_TOKEN_EXPIRE_DAYS))
    
    return {"access_token":access_token,"refresh_token":refresh_token}


@auth_endpoints.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")

        new_access = create_token(
            {"sub": user_id, "type": "access"},
            expire_minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        new_refresh = create_token(
            {"sub": user_id, "type": "refresh"},
            expire_minutes=int(settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return {
            "access_token": new_access,
            "refresh_token": new_refresh
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")