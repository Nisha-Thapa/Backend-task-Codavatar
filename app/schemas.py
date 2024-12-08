from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class VirtualPhoneNumberCreate(BaseModel):
    number: str
    user_id: int

class VirtualPhoneNumberResponse(BaseModel):
    id: int
    number: str

    class Config:
        orm_mode = True