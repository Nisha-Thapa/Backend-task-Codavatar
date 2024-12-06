from pydantic import BaseModel, field_validator


class VirtualPhoneNumberCreate(BaseModel):
    phone_number: int

    @field_validator("phone_number")
    def validate_nepali_phone_number(cls, value):
        """simple validator to check if the provided phone number simply follows nepali pattern or not. (Can be changed according to need)"""
        phone_str = str(value)
        if len(phone_str) != 10 or not phone_str.startswith("9"):
            raise ValueError("Invalid Nepali phone number..")
        return value



class VirtualPhoneNumberDisplay(VirtualPhoneNumberCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
