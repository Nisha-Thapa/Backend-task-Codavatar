from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal
from app.utils import get_db
from typing import List


router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.get(
    "/users/{user_id}/virtual-phone-numbers",
    response_model=List[schemas.VirtualPhoneNumber],
)
def read_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
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
