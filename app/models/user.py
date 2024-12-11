# app/models/user.py
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str = Field(nullable=False, unique=True) 
    password: str = Field(nullable=False)