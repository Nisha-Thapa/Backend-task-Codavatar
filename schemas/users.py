from typing import Optional
from pydantic import BaseModel, field_validator, EmailStr


class UserDisplay(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    email: EmailStr



class UserCreate(UserDisplay):
    password: str



class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
