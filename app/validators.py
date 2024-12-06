from fastapi import HTTPException


def validate_phone_number(value: str) -> str:
    value = value.replace(" ", "")
    if value.startswith("+"):
        if not value[1:].isdigit():
            raise HTTPException(
                status_code=400,
                detail="Phone number must contain only digits after the '+' sign.",
            )
    elif not value.isdigit():
        raise HTTPException(
            status_code=400, detail="Phone number must contain only digits."
        )

    count = len(value)
    if count < 10 or count > 15:
        raise HTTPException(
            status_code=400,
            detail=f"Phone number length must be between 10 and 15 digits. Your length is {count}.",
        )

    return value
