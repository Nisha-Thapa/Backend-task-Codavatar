from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def get_virtual_phone_numbers(db: Session, user_id: int):

    return db.query(models.VirtualPhoneNumber).filter(models.VirtualPhoneNumber.user_id == user_id).all()

def create_virtual_phone_number(db: Session, virtual_phone_number: schemas.VirtualPhoneNumberCreate, user_id: int):
    # Check if the phone number already exists for the user
    existing_number = (
        db.query(models.VirtualPhoneNumber)
        .filter(
            models.VirtualPhoneNumber.number == virtual_phone_number.number,
            models.VirtualPhoneNumber.user_id == user_id,
        )
        .first()
    )
    if existing_number:
        raise HTTPException(status_code=400, detail="Phone number already exists for this user.")

    db_virtual_phone_number = models.VirtualPhoneNumber(**virtual_phone_number.dict(), user_id=user_id)
    db.add(db_virtual_phone_number)
    db.commit()
    db.refresh(db_virtual_phone_number)
    return db_virtual_phone_number

