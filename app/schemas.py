from pydantic import BaseModel, EmailStr, Field
from typing import List

class VirtualPhoneNumberBase(BaseModel):
    number: str

class VirtualPhoneNumberCreate(VirtualPhoneNumberBase):
    number: str = Field(..., regex=r"^\+?[1-9]\d{1,14}$") # Using Regex for proper number format

class VirtualPhoneNumber(VirtualPhoneNumberBase):
    id: int
    user_id: int

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
    virtual_phone_numbers: List[VirtualPhoneNumber] = []

    class Config:
        orm_mode = True
