from fastapi import HTTPException
from auth_utils import verify_access_token


# JWT token extraction and validation
def get_current_user(token: str):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
