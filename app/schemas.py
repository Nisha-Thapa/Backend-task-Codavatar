from pydantic import BaseModel,  validator
from typing import List, Optional

class VirtualPhoneNumberBase(BaseModel):
    number: str

    @validator("number")
    def validate_phone_number(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return value

class VirtualPhoneNumberCreate(VirtualPhoneNumberBase):
    pass

class VirtualPhoneNumber(VirtualPhoneNumberBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    virtual_phone_numbers: List[VirtualPhoneNumber] = []

    class Config:
        orm_mode = True
