from app.database import SessionLocal
from fastapi import HTTPException

def raise_http_exception(status_code: int, detail: str):
    """
    Helper function to raise an HTTPException with a given status code and detail message.

    Args:
        status_code (int): The status code to return (e.g., 400, 404).
        detail (str): The detail message explaining the error.
    
    Raises:
        HTTPException: The HTTPException with the provided status code and detail.
    """
    raise HTTPException(status_code=status_code, detail=detail)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
