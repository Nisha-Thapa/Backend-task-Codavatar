from fastapi import HTTPException
from app.utils import raise_http_exception


def validate_phone_number(value: str) -> str:
    """
    Validates a phone number based on the following criteria:
    - If the number starts with a '+', the part after the '+' must be digits only.
    - If the number does not start with a '+', it must contain only digits.
    - The length of the phone number must be between 10 and 15 digits, inclusive.

    Args:
        value (str): The phone number to validate.

    Raises:
        HTTPException: If the phone number is invalid, an HTTPException is raised with a detailed message.
            - If it contains non-digit characters after a '+', the exception message will be:
              "Phone number must contain only digits after the '+' sign."
            - If it contains non-digit characters without a '+', the exception message will be:
              "Phone number must contain only digits."
            - If the length is not between 10 and 15 digits, the exception message will specify the length.

    Returns:
        str: The validated phone number (with spaces removed).
    """
    value = value.replace(" ", "")
    if value.startswith("+"):
        if not value[1:].isdigit():
            raise_http_exception(
                400,
                f"Phone number must contain only digits after the '+' sign.",
            )
    elif not value.isdigit():
        raise_http_exception(400, f"Phone number must contain only digits.")

    count = len(value)
    if count < 10 or count > 15:
        raise_http_exception(
            400,
            f"Phone number length must be between 10 and 15 digits. Your length is {count}.",
        )

    return value
