from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from database import get_session
from models import user as user_model
from models import phone as phone_model
from schemas.phone import VirtualPhoneNumberCreate, VirtualPhoneNumberDisplay
from utils.encode_decode import get_current_user



router = APIRouter()


@router.post('/add-phone-number', response_model=VirtualPhoneNumberDisplay)
def add_phone_number(
    request: VirtualPhoneNumberCreate,
    current_user: user_model.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please login first"
            )
        
        new_phone_number = phone_model.VirtualPhoneNumber(
            user_id=current_user.id,
            phone_number = request.phone_number
        )

        session.add(new_phone_number)
        session.commit()
        session.refresh(new_phone_number)
        return new_phone_number
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e


@router.get('/phone-numbers', response_model=List[VirtualPhoneNumberDisplay])
def get_user_phone_numbers(
    current_user: user_model.User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please login first"
            )
        
        phone_numbers = session.query(phone_model.VirtualPhoneNumber).filter_by(user_id=current_user.id).all()
        return phone_numbers
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
