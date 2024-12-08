from app.database import SessionLocal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models
from typing import NoReturn, Generator



def raise_http_exception(status_code: int, detail: str) -> NoReturn:
    """
    Raises an HTTPException with the provided status code and detail.

    Args:
        status_code: The HTTP status code to be used.
        detail: The detail message to be used in the HTTPException.

    Returns:
        NoReturn: This function never returns and raises an HTTPException.
    """
    raise HTTPException(status_code=status_code, detail=detail)


def get_user_or_raise(db: Session, user_id: int) -> models.User:
    """
    Retrieves a user from the database.

    Args:
        db: The database session.
        user_id: The ID of the user to be retrieved.

    Returns:
        The retrieved user.

    Raises:
        HTTPException: If the user is not found, an HTTPException is raised with a 404 status code.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise raise_http_exception(
            404, f"User with id {user_id} not found. Please create a user first."
        )
    return user



def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session.

    This is a context manager that yields a database session. The session is
    closed when the context manager is exited.

    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
