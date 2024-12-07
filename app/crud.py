from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from . import models, schemas
from app.utils import raise_http_exception


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    """
    Create a new user in the system

    This function creates a new user in the database with the provided name and email.

    Args:
        db (Session): The database session object.
        user (schemas.UserCreate): The user data to create.

    Returns:
        models.User: The created user object with all the fields from the database.
    """
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_virtual_phone_number_by_id_and_user(
    db: Session, phone_number_id: int, user_id: int
):
    """
    Retrieve a virtual phone number by its ID and the associated user ID.

    This function retrieves a virtual phone number from the database by its unique ID
    and the associated user ID.

    Args:
        db (Session): The database session object.
        phone_number_id (int): The unique identifier for the virtual phone number.
        user_id (int): The unique identifier for the user associated with the virtual phone number.

    Returns:
        models.VirtualPhoneNumber: The retrieved virtual phone number object or None if not found.
    """
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
):
    """
    Create a new virtual phone number for a user.

    This function checks if the given virtual phone number already exists for the
    specified user by querying the database. If the number already exists, it raises
    a `400` error indicating that the phone number is already associated with the user.
    If the number doesn't exist, the function creates a new virtual phone number and
    associates it with the user in the database.

    Args:
        db (Session): The database session used to query and interact with the database.
        virtual_phone_number (schemas.VirtualPhoneNumberCreate): The data for creating the virtual phone number.
        user_id (int): The ID of the user to associate the virtual phone number with.

    Raises:
        HTTPException:
            - If the phone number already exists for the user, raises a `400` error.

    Returns:
        models.VirtualPhoneNumber: The created virtual phone number with details saved in the database.
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
        raise_http_exception(
            400,f"Phone number already exists for this user."
        )

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
    # Check if the new number already exists for the user
    existing_number = (
        db.query(models.VirtualPhoneNumber)
        .filter(
            models.VirtualPhoneNumber.number == new_number,
            models.VirtualPhoneNumber.user_id == user_id,
        )
        .first()
    )
    
    if existing_number:
        raise_http_exception(
            400,f"Phone number already exists for this user."
        )

    
    # Get the current phone number object
    phone_number = db.query(models.VirtualPhoneNumber).filter(
        models.VirtualPhoneNumber.id == phone_number_id,
        models.VirtualPhoneNumber.user_id == user_id,
    ).first()

    if not phone_number:
        raise_http_exception(
            404,f"Phone number with ID {phone_number_id} not found for user {user_id}",
        )

    try:
        phone_number.number = new_number
        db.commit()
        db.refresh(phone_number)

        return phone_number

    except SQLAlchemyError as e:
        db.rollback()
        raise e
