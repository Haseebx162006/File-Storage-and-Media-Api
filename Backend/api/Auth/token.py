from datetime import datetime, timedelta
from jose import jwt, JWTError
from Auth.config import settings
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from api.database import get_db
from sqlalchemy.orm import Session
from model.User import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_token(data: dict, expire_minutes: int):
    """
    Create JWT token with expiration
    expire_minutes: int, number of minutes until token expires
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(expire_minutes))
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create JWT token"
        )

    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized user",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise credential_exception

    return user
