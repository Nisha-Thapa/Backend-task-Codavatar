from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

def get_user_by_id(db: Session, user_id: int):
    """
    Fetch a user by ID. Raise an HTTP exception if the user does not exist.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or user.deleted_status :
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Create a new user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Soft delete user (set deleted_status to True)
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.deleted_status = True
        db.commit()
        return user
    return None

# Get all users, excluding deleted ones
def get_all_users(db: Session):
    return db.query(models.User).filter(models.User.deleted_status == False).all()

def create_virtual_phone_number(db: Session, number: schemas.VirtualPhoneNumberCreate, user_id: int):
    """
    Create a new virtual phone number for a user. 
    Validate user existence and ensure the number is unique.
    """
    # Validate user existence
    user = get_user_by_id(db, user_id)
    
    # Check if the phone number already exists
    existing_number = db.query(models.VirtualPhoneNumber).filter(models.VirtualPhoneNumber.number == number.number).first()
    if existing_number:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    
    # Create the new virtual phone number
    db_number = models.VirtualPhoneNumber(number=number.number, user_id=user_id)
    db.add(db_number)
    db.commit()
    db.refresh(db_number)
    return db_number

def get_virtual_phone_numbers(db: Session, user_id: int):
    """
    Retrieve all virtual phone numbers for a specific user.
    Validate user existence before querying.
    """
    # Validate user existence
    user = get_user_by_id(db, user_id)
    
    # Query and return the virtual phone numbers
    return db.query(models.VirtualPhoneNumber).filter(models.VirtualPhoneNumber.user_id == user.id).all()
