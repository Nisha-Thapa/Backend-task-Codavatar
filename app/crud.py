from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_virtual_phone_number(db: Session, number: str, user_id: int):
    db_number = models.VirtualPhoneNumber(number=number, user_id=user_id)
    db.add(db_number)
    db.commit()
    db.refresh(db_number)
    return db_number

def get_virtual_phone_numbers(db: Session, user_id: int):
    return db.query(models.VirtualPhoneNumber).filter(models.VirtualPhoneNumber.user_id == user_id).all()
