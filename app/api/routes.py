from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal
from app.utils import get_db
from typing import List


router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> schemas.User:
    """
    Create a new user in the system

    Args:
        user (schemas.UserCreate): The user data to create.
        db (Session): The database session object.

    Raises:
        HTTPException: If the user already exists.

    Returns:
        schemas.User: The created user object with all the fields from the database.
    """
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"Email  {user.email} is already registered.Use other email.",
        )

    return crud.create_user(db=db, user=user)


@router.get("/users/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)) -> List[schemas.User]:
    """
    Retrieve a list of all users in the system.

    Args:
        db (Session): The database session object.

    Returns:
        List[schemas.User]: A list of all users in the system.
    """
    return crud.get_users(db)


@router.get(
    "/users/{user_id}/virtual-phone-numbers",
    response_model=List[schemas.VirtualPhoneNumber],
)
def read_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a list of virtual phone numbers associated with a specific user.

    This endpoint fetches all virtual phone numbers that belong to the user identified by the
    provided `user_id`. If no phone numbers are found for the user, a 404 error is raised.

    Args:
        user_id (int): The ID of the user whose virtual phone numbers are to be fetched.
        db (Session, optional): The database session used for querying the database.

    Returns:
        List[schemas.VirtualPhoneNumber]: A list of virtual phone numbers associated with the user.

    Raises:
        HTTPException: If no phone numbers are found for the given user ID, a 404 error is raised
        with a message indicating that no phone numbers were found for that user.
    """
    numbers = crud.get_virtual_phone_numbers(db, user_id=user_id)
    if not numbers:
        raise HTTPException(
            status_code=404,
            detail=f"No phone numbers found for user having user_id: {user_id}.Please Add a phone number",
        )
    return numbers


@router.post(
    "/users/{user_id}/virtual-phone-numbers", response_model=schemas.VirtualPhoneNumber
)
def create_virtual_phone_number(
    user_id: int,
    phone_number: schemas.VirtualPhoneNumberCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new virtual phone number for a specific user.

    This endpoint allows the creation of a virtual phone number for a user identified by
    the provided `user_id`. If the user does not exist, a 404 error is returned, prompting
    the creation of the user first.

    Args:
        user_id (int): The ID of the user to associate with the virtual phone number.
        phone_number (schemas.VirtualPhoneNumberCreate): The phone number data to create a new virtual phone number.
        db (Session, optional): The database session used to interact with the database.

    Returns:
        schemas.VirtualPhoneNumber: The newly created virtual phone number associated with the user.

    Raises:
        HTTPException: If the user with the provided `user_id` does not exist, a 404 error is raised
        indicating that the user must be created first.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} not found. Please Create a user First",
        )

    return crud.create_virtual_phone_number(
        db, virtual_phone_number=phone_number, user_id=user_id
    )


@router.patch(
    "/users/{user_id}/virtual_phone_numbers/{phone_number_id}",
    response_model=schemas.VirtualPhoneNumber,
)
def update_phone_number(
    user_id: int,
    phone_number_id: int,
    phone_number_data: schemas.VirtualPhoneNumberUpdate,
    db: Session = Depends(get_db),
):
    """
    Update the phone number of a specific user.

    This endpoint allows updating the virtual phone number associated with a user.
    It verifies if the user and the phone number exist. If they do, the phone number 
    is updated to the new value provided. The request will return the updated phone 
    number if successful.

    Args:
    - user_id (int): The ID of the user whose phone number is to be updated.
    - phone_number_id (int): The ID of the virtual phone number to be updated.
    - phone_number_data (schemas.VirtualPhoneNumberUpdate): The data for updating the phone number.
    - db (Session): The database session dependency for performing database operations.

    Returns:
    - VirtualPhoneNumber: The updated virtual phone number details.

    Raises:
    - HTTPException: 
        - 404: If the user or phone number is not found.
        - 400: If the phone number format is invalid.
    """

    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    phone_number = crud.get_virtual_phone_number_by_id_and_user(
        db, phone_number_id, user_id
    )
    if phone_number is None:
        raise HTTPException(
            status_code=404,
            detail=f"Phone number with ID {phone_number_id} not found for user {user_id}",
        )

    updated_phone_number = crud.update_phone_number_by_user(
        db, user_id, phone_number_id, phone_number_data.number
    )

    if updated_phone_number is None:
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    return updated_phone_number