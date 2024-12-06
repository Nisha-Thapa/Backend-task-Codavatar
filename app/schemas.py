from pydantic import BaseModel, EmailStr, Field
from typing import List
import datetime

class VirtualPhoneNumberBase(BaseModel):
    number: str

class VirtualPhoneNumberCreate(VirtualPhoneNumberBase):
    number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$") # Using Regex for proper number format

class VirtualPhoneNumber(VirtualPhoneNumberBase):
    id: int
    user_id: int
    created_at: datetime.datetime  # Add created_at field to the Pydantic model

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    name: str = Field(..., max_length=50, min_length=2)
    email: EmailStr  # Validates email format

class User(UserBase):
    id: int
    created_at: datetime.datetime  # Add created_at field here as well
    virtual_phone_numbers: List[VirtualPhoneNumber] = []

    class Config:
        orm_mode = True
