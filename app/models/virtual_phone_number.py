# app/models/virtual_phone_number.py
from sqlmodel import SQLModel, Field

class VirtualPhoneNumber(SQLModel, table=True):
    id: int = Field(primary_key=True)
    number: str = Field(unique=True)
    user_id: int
