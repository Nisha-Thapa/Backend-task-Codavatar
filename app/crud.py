from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from . import models, schemas
from app.utils import raise_http_exception
from typing import List


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    try:
        db_user = models.User(name=user.name, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_virtual_phone_number_by_id_and_user(
    db: Session, phone_number_id: int, user_id: int
):
    return (
        db.query(models.VirtualPhoneNumber)
        .filter(
            models.VirtualPhoneNumber.id == phone_number_id,
            models.VirtualPhoneNumber.user_id == user_id,
        )
        .first()
    )


def get_virtual_phone_numbers(db: Session, user_id: int):

    return (
        db.query(models.VirtualPhoneNumber)
        .filter(models.VirtualPhoneNumber.user_id == user_id)
        .all()
    )


def create_virtual_phone_number(
    db: Session, virtual_phone_number: schemas.VirtualPhoneNumberCreate, user_id: int
) -> models.VirtualPhoneNumber:
    """
    Creates a virtual phone number for the specified user.

    Args:
        db: The database session.
        virtual_phone_number: The virtual phone number data.
        user_id: The ID of the user for which the phone number is to be created.

    Returns:
        The created virtual phone number.

    Raises:
        HTTPException: If the phone number already exists for the specified user.
    """
    existing_number = (
        db.query(models.VirtualPhoneNumber)
        .filter(
            models.VirtualPhoneNumber.number == virtual_phone_number.number,
            models.VirtualPhoneNumber.user_id == user_id,
        )
        .first()
    )
    if existing_number:
        raise_http_exception(400, f"Phone number already exists for this user.")

    db_virtual_phone_number = models.VirtualPhoneNumber(
        **virtual_phone_number.dict(), user_id=user_id
    )
    db.add(db_virtual_phone_number)
    db.commit()
    db.refresh(db_virtual_phone_number)
    return db_virtual_phone_number


def update_phone_number_by_user(
    db: Session, user_id: int, phone_number_id: int, new_number: str
):
    """
    Updates the phone number for a specific user.

    Args:
        db (Session): The SQLAlchemy database session.
        user_id (int): The ID of the user whose phone number is to be updated.
        phone_number_id (int): The ID of the phone number to be updated.
        new_number (str): The new phone number to update to.

    Returns:
        models.VirtualPhoneNumber: The updated VirtualPhoneNumber object.

    """    
    existing_number = (
        db.query(models.VirtualPhoneNumber)
        .filter(
            models.VirtualPhoneNumber.number == new_number,
            models.VirtualPhoneNumber.user_id == user_id,
        )
        .first()
    )

    if existing_number:
        raise_http_exception(400, f"Phone number already exists for this user.")

    phone_number = (
        db.query(models.VirtualPhoneNumber)
        .filter(
            models.VirtualPhoneNumber.id == phone_number_id,
            models.VirtualPhoneNumber.user_id == user_id,
        )
        .first()
    )

    if not phone_number:
        raise_http_exception(
            404,
            f"Phone number with ID {phone_number_id} not found for user {user_id}",
        )

    try:
        phone_number.number = new_number
        db.commit()
        db.refresh(phone_number)

        return phone_number

    except SQLAlchemyError as e:
        db.rollback()
        raise e



