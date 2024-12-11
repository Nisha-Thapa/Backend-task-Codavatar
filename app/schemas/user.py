from pydantic import BaseModel

# Schema for creating a new user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Schema for user response (excluding sensitive fields)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True  # Enable ORM mode for automatic conversion from SQLAlchemy model

# Schema for user update (if needed in the future)
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
