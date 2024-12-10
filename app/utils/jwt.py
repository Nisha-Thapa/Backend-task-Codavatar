import os
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union

# JWT Token expiration (default 15 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Can adjust as needed

# Secret key for JWT encoding/decoding
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

# Create JWT Token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decode JWT Token
def verify_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception