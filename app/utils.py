from app.database import SessionLocal
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models

def raise_http_exception(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)


def get_user_or_raise(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise raise_http_exception(
            404,f"User with id {user_id} not found. Please create a user first."
        )
    return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
