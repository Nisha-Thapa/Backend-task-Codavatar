from pydantic import BaseModel
from typing import List, Optional

class VirtualPhoneNumberBase(BaseModel):
    number: str

class VirtualPhoneNumberCreate(VirtualPhoneNumberBase):
    pass

class VirtualPhoneNumber(VirtualPhoneNumberBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    virtual_phone_numbers: List[VirtualPhoneNumber] = []

    class Config:
        orm_mode = True
