from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal
from app.utils import get_db, raise_http_exception, get_user_or_raise
from typing import List


router = APIRouter()


@router.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    """
    Creates a new user in the database.

    Args:
        user: The user to be created.
        db: The database session.

    Returns:
        The created user.
    """
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise_http_exception(
            400, f"Email {user.email} is already registered. Use another email."
        )
    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User], tags=["users"])
def get_users(db: Session = Depends(get_db)) -> List[schemas.User]:
    """
    Retrieves all users from the database.

    Raises:
        HTTPException: If there are no users in the database, an HTTPException is raised with a 404 status code.
        HTTPException: If an SQLAlchemy error occurs, an HTTPException is raised with a 500 status code.

    Returns:
        List[schemas.User]: A list of all users in the database.
    """
    try:
        users = crud.get_users(db)
        if not users:
            raise_http_exception(404, "No users found.")
        return users
    except SQLAlchemyError:
        raise_http_exception(500, "An error occurred while retrieving users.")


@router.get(
    "/users/{user_id}/virtual-phone-numbers",
    response_model=List[schemas.VirtualPhoneNumber],
    tags=["virtual phone numbers"],
)
def read_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves virtual phone numbers for a specified user.

    Args:
        user_id: The ID of the user whose phone numbers are to be retrieved.
        db: The database session.

    Returns:
        A list of virtual phone numbers for the user.
    """
    get_user_or_raise(db, user_id)
    numbers = crud.get_virtual_phone_numbers(db, user_id=user_id)
    if not numbers:
        raise_http_exception(
            404,
            f"No phone numbers found for user having user_id: {user_id}. Please add a phone number.",
        )
    return numbers


@router.post(
    "/users/{user_id}/virtual-phone-numbers",
    response_model=schemas.VirtualPhoneNumber,
    tags=["virtual phone numbers"],
)
def create_virtual_phone_number(
    user_id: int,
    phone_number: schemas.VirtualPhoneNumberCreate,
    db: Session = Depends(get_db),
):
    """
    Creates a virtual phone number for a specified user.

    Args:
        user_id: The ID of the user for which the phone number is to be created.
        phone_number: The phone number data including the number.
        db: The database session.

    Returns:
        The created virtual phone number.
    """
    get_user_or_raise(db, user_id)
    return crud.create_virtual_phone_number(
        db, virtual_phone_number=phone_number, user_id=user_id
    )


@router.patch(
    "/users/{user_id}/virtual_phone_numbers/{phone_number_id}",
    response_model=schemas.VirtualPhoneNumber,
    tags=["virtual phone numbers"],
)
def update_phone_number(
    user_id: int,
    phone_number_id: int,
    phone_number_data: schemas.VirtualPhoneNumberUpdate,
    db: Session = Depends(get_db),
):
    """
    Updates an existing virtual phone number of a specified user.

    Args:
        user_id: The ID of the user whose phone number is to be updated.
        phone_number_id: The ID of the phone number to be updated.
        phone_number_data: The phone number data including the new number.
        db: The database session.

    Returns:
        The updated virtual phone number.
    """
    get_user_or_raise(db, user_id)

    phone_number = crud.get_virtual_phone_number_by_id_and_user(
        db, phone_number_id, user_id
    )
    if phone_number is None:
        raise_http_exception(
            404, f"Phone number with ID {phone_number_id} not found for user {user_id}"
        )

    updated_phone_number = crud.update_phone_number_by_user(
        db, user_id, phone_number_id, phone_number_data.number
    )

    return updated_phone_number
