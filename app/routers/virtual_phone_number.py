from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models import VirtualPhoneNumber, User
from app.schemas.virtual_phone_number import VirtualPhoneNumberCreate, VirtualPhoneNumberResponse

router = APIRouter()

# Endpoint to retrieve a list of virtual phone numbers
@router.get("/virtual-phone-numbers/{user_id}", response_model=list[VirtualPhoneNumberResponse])
def get_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    phone_numbers = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.user_id == user_id).all()
    if not phone_numbers:
        raise HTTPException(status_code=404, detail="No virtual phone numbers found for this user")
    return phone_numbers

# Endpoint to create a new virtual phone number
@router.post("/virtual-phone-numbers", response_model=VirtualPhoneNumberResponse)
def create_virtual_phone_number(phone_number: VirtualPhoneNumberCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == phone_number.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_virtual_phone_number = VirtualPhoneNumber(**phone_number.dict())
    db.add(db_virtual_phone_number)
    db.commit()
    db.refresh(db_virtual_phone_number)
    return db_virtual_phone_number
