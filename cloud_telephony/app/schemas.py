from pydantic import BaseModel, constr, Field

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=100)

# User Login Schema
class UserLogin(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=100)

# Token Response Schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Request schema for creating a phone number
class VirtualPhoneNumberCreate(BaseModel):
    phone_number: str = Field(..., example="123-456-7890")

# Response schema for virtual phone numbers
class VirtualPhoneNumberResponse(BaseModel):
    id: int
    phone_number: str
    user_id: int
