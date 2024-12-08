from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import get_db

router = APIRouter()

@router.get("/users/{user_id}", response_model=list[schemas.VirtualPhoneNumberResponse])
def get_user_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.phone_numbers

@router.post("/", response_model=schemas.VirtualPhoneNumberResponse)
def create_virtual_phone_number(phone_number: schemas.VirtualPhoneNumberCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == phone_number.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_phone_number = models.VirtualPhoneNumber(number=phone_number.number, owner=user)
    db.add(db_phone_number)
    db.commit()
    db.refresh(db_phone_number)
    return db_phone_number