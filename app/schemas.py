from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional

from .validators import validate_phone_number


class VirtualPhoneNumberBase(BaseModel):
    number: str

    @validator("number")
    def validate_phone_number(cls, value):
        return validate_phone_number(value)


class VirtualPhoneNumberCreate(VirtualPhoneNumberBase):
    pass


class VirtualPhoneNumberUpdate(BaseModel):
    number: str

    @validator("number")
    def validate_phone_number(cls, value):
        return validate_phone_number(value)


class VirtualPhoneNumber(VirtualPhoneNumberBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    virtual_phone_numbers: List[VirtualPhoneNumber] = []

    class Config:
        orm_mode = True
