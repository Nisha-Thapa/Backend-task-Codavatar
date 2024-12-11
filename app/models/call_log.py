# app/models/call_log.py
from sqlmodel import SQLModel, Field

class CallLog(SQLModel, table=True):
    id: int = Field(primary_key=True)
    virtual_phone_number_id: int
    call_timestamp: str
    duration: int
