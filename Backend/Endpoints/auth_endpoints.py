from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from Backend.Auth.Security import hash_password

from Backend.database import get_db
from Backend.Auth.Crud import create_user, search_with_email
from Backend.Schemas.User import (
    Create_User_Schema,
    TokenResponse
)
from Backend.Auth.Security import verify_password
from Backend.Auth.token import create_token
from Backend.Auth.config import settings

auth_endpoints = APIRouter(prefix="/api/auth", tags=["Authentication"])


# =========================
# SIGNUP
# =========================
@auth_endpoints.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: Create_User_Schema, db: Session = Depends(get_db)):
    existing_user = search_with_email(user.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    hashed_password_1 =hash_password(user.password)
    new_user = create_user(
        email=user.email,
        password=hashed_password_1,
        name=user.name,
        db=db
    )

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }


# =========================
# LOGIN
# =========================
@auth_endpoints.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = search_with_email(form_data.username, db)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_token(
        data={"sub": str(user.id), "type": "access"},
        expire_minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_token(
        data={"sub": str(user.id), "type": "refresh"},
        expire_minutes=int(settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


# =========================
# REFRESH TOKEN
# =========================
@auth_endpoints.post("/refresh", response_model=TokenResponse)
def refresh_token_endpoint(request_body: dict, db: Session = Depends(get_db)):
    refresh_token = request_body.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required"
        )
    
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")

        new_access_token = create_token(
            data={"sub": user_id, "type": "access"},
            expire_minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        new_refresh_token = create_token(
            data={"sub": user_id, "type": "refresh"},
            expire_minutes=int(settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
