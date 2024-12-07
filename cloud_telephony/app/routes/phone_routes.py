from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, VirtualPhoneNumber
from schemas import VirtualPhoneNumberCreate, VirtualPhoneNumberResponse
import logging

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize phone_router
phone_router = APIRouter()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@phone_router.get("/users/{user_id}/phone_numbers", response_model=list[VirtualPhoneNumberResponse])
def get_user_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching phone numbers for user_id: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error("User not found.")
        raise HTTPException(status_code=404, detail="User not found")
    phone_numbers = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.user_id == user_id).all()
    logger.info("Phone numbers fetched successfully.")
    return phone_numbers


@phone_router.post("/users/{user_id}/phone_numbers", response_model=VirtualPhoneNumberResponse)
def create_virtual_phone_number(user_id: int, phone_data: VirtualPhoneNumberCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating phone number for user_id: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error("User not found.")
        raise HTTPException(status_code=404, detail="User not found")

    new_phone = VirtualPhoneNumber(phone_number=phone_data.phone_number, user_id=user_id)
    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)
    logger.info("Phone number created successfully.")
    return new_phone
