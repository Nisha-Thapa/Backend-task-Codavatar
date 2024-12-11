from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models import VirtualPhoneNumber, User
from app.schemas.virtual_phone_number import VirtualPhoneNumberCreate, VirtualPhoneNumberResponse
import re
router = APIRouter()


# Endpoint to retrieve a list of virtual phone numbers
@router.get("/virtual-phone-numbers/{user_id}", response_model=list[VirtualPhoneNumberResponse])
def get_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    phone_numbers = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.user_id == user_id).all()
    if not phone_numbers:
        raise HTTPException(status_code=404, detail="No virtual phone numbers found for this user")
    return phone_numbers

# Function to validate the phone number
def validate_phone_number(phone_number: str) -> bool:
    return bool(re.match(r'^\d{10}$', phone_number))

# Endpoint to create a new virtual phone number
@router.post("/virtual-phone-numbers", response_model=VirtualPhoneNumberResponse)
def create_virtual_phone_number(
    phone_number: VirtualPhoneNumberCreate, db: Session = Depends(get_db)
):
    # Check if the user exists
    db_user = db.query(User).filter(User.id == phone_number.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the phone number already exists in the database
    existing_phone_number = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.number == phone_number.number).first()
    if existing_phone_number:
        raise HTTPException(status_code=400, detail="Phone number already in use")
    
    # Validate phone number format (must be 10 digits)
    if not validate_phone_number(phone_number.number):
        raise HTTPException(status_code=400, detail="Phone number must be exactly 10 digits")

    # Create a new virtual phone number instance with the phone number provided by the user
    db_virtual_phone_number = VirtualPhoneNumber(
        number=phone_number.number, user_id=phone_number.user_id
    )

    # Add to the database and commit
    db.add(db_virtual_phone_number)
    db.commit()
    db.refresh(db_virtual_phone_number)

    # Return the virtual phone number details
    return db_virtual_phone_number