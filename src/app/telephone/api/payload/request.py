from pydantic import BaseModel, field_validator, Field
from fastapi import status

from src.app.core.exception.generic_app_exception import GenericAppException


class VirtualPhoneNumberCreate(BaseModel):
    phone_number: str

    class Config:
        from_attributes = True

    @field_validator("phone_number", mode="before")
    def validate_mobile(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise GenericAppException(
                status.HTTP_400_BAD_REQUEST,
                "Phone Number must be 10 digit number.",
            )
        return value


class MakeCallRequest(BaseModel):
    source_number_id: int = Field(
        ..., description="ID of the source virtual phone number"
    )
    destination_phone_number: str = Field(
        ..., description="The destination phone number"
    )

    @field_validator("destination_phone_number", mode="before")
    def validate_mobile(cls, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise GenericAppException(
                status.HTTP_400_BAD_REQUEST,
                "Phone Number must be 10 digit number.",
            )
        return value
