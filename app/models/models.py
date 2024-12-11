from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    phone_numbers: List["VirtualPhoneNumber"] = Relationship(back_populates="user")

class VirtualPhoneNumber(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    phone_number: str
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="phone_numbers")
    call_logs: List["CallLog"] = Relationship(back_populates="virtual_phone_number")

class CallLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    call_time: str
    duration: int
    virtual_phone_number_id: int = Field(default=None, foreign_key="virtualphonenumber.id")
    virtual_phone_number: VirtualPhoneNumber = Relationship(back_populates="call_logs")
