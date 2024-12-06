from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal
from typing import List 


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/{user_id}/virtual-phone-numbers", response_model=List[schemas.VirtualPhoneNumber]) 
def read_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    numbers = crud.get_virtual_phone_numbers(db, user_id=user_id)
    if not numbers:
        raise HTTPException(status_code=404, detail="No phone numbers found for user.")
    return numbers


@router.post("/users/{user_id}/virtual-phone-numbers", response_model=schemas.VirtualPhoneNumber)
def create_virtual_phone_number(user_id: int, phone_number: schemas.VirtualPhoneNumberCreate, db: Session = Depends(get_db)):
    return crud.create_virtual_phone_number(db, virtual_phone_number=phone_number, user_id=user_id)

