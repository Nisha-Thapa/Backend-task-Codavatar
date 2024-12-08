from pydantic import BaseModel
from datetime import datetime

from src.app.users.api.payload.response import User


class VirtualNumberList(User):
    phone_numbers: list[str]


class VirtualPhoneNumberResponse(BaseModel):
    id: int
    user_id: int
    phone_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CallLogResponse(BaseModel):
    id: int | None = None
    phone_number_id: int
    destination_phone_number: str
    call_start_time: datetime
    call_duration_seconds: int
    direction: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VirtualPhoneNumberDetailList(BaseModel):
    id: int
    phone_number: str
    user_name: str
    email: str
    call_logs: list[CallLogResponse]

    class Config:
        from_attributes = True
