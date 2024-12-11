

from pydantic import BaseModel

# Request Schema: Used when creating a virtual phone number
class VirtualPhoneNumberCreate(BaseModel):
    user_id: int
    number:str  
    
    class Config:
        orm_mode = True  

# Response Schema: Used for returning the virtual phone number details after creation
class VirtualPhoneNumberResponse(BaseModel):
    id: int  
    number: str  
    user_id: int 

    class Config:
        orm_mode = True 
