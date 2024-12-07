import re
from pydantic import BaseModel, Field, field_validator
from fastapi import status

from src.app.users.choices import Genders
from src.app.core.exception.generic_app_exception import GenericAppException


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=5)
    email: str
    address: str
    gender: Genders

    class Config:
        from_attributes = True

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if value:
            email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.fullmatch(email_regex, value):
                raise GenericAppException(
                    status.HTTP_400_BAD_REQUEST,
                    "Invalid email format.",
                )
        return value


class UserUpdateRequest(BaseModel):
    id: int
    name: str | None = None
    email: str | None = None
    address: str | None = None
    gender: Genders | None = None

    class Config:
        from_attributes = True

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        if value:
            email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.fullmatch(email_regex, value):
                raise GenericAppException(
                    status.HTTP_400_BAD_REQUEST,
                    "Invalid email format.",
                )
        return value
