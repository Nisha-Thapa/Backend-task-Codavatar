from pydantic import BaseModel

class VirtualPhoneNumberBase(BaseModel):
    phone_number: str

class VirtualPhoneNumberCreate(VirtualPhoneNumberBase):
    pass

class VirtualPhoneNumberResponse(VirtualPhoneNumberBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
