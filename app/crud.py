from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_virtual_phone_number_by_id_and_user(db: Session, phone_number_id: int, user_id: int):
    return db.query(models.VirtualPhoneNumber).filter(
        models.VirtualPhoneNumber.id == phone_number_id,
        models.VirtualPhoneNumber.user_id == user_id
    ).first()


def get_virtual_phone_numbers(db: Session, user_id: int):

    return db.query(models.VirtualPhoneNumber).filter(models.VirtualPhoneNumber.user_id == user_id).all()

def create_virtual_phone_number(db: Session, virtual_phone_number: schemas.VirtualPhoneNumberCreate, user_id: int):
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

def update_phone_number_by_user(db: Session, user_id: int, phone_number_id: int, new_number: str):
    try:
        phone_number = db.query(models.VirtualPhoneNumber).filter(
            models.VirtualPhoneNumber.id == phone_number_id,
            models.VirtualPhoneNumber.user_id == user_id
        ).first()

        if phone_number is None:
            return None 
        
        phone_number.number = new_number
        db.commit()  
        db.refresh(phone_number) 
        
        return phone_number  
    
    except SQLAlchemyError as e:
        db.rollback()  
        raise e
