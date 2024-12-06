from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/phone-numbers/", response_model=List[schemas.VirtualPhoneNumber])
def list_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    numbers = crud.get_virtual_phone_numbers(db, user_id=user_id)
    if not numbers:
        raise HTTPException(status_code=404, detail="No phone numbers found for user.")
    return numbers

@router.post("/phone-numbers/", response_model=schemas.VirtualPhoneNumber)
def create_phone_number(number: schemas.VirtualPhoneNumberCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_virtual_phone_number(db, number=number.number, user_id=user_id)