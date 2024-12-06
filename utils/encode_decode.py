import os, jwt

from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status

from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer

from pydantic import EmailStr

from schemas.users import TokenData, UserDisplay


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




def get_password_hash(password):
    return pwd_context.hash(password)



def get_user(db, email: EmailStr):
    if email in db:
        user_dict = db[email]
        return UserDisplay(**user_dict)
    


def authenticate_user(db, email: EmailStr, password: str):
    user = get_user(db, email)

    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return True



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('JWT_SECRET_KEY'), os.getenv('ALGORITHM'))
    return encoded_jwt



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], database):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=os.getenv('ALGORITHM'))
        email: EmailStr = payload.get('sub')

        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(db=database, email=token_data.email)

    if user is None:
        raise credentials_exception
    return user

