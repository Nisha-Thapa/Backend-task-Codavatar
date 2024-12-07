from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session


from fastapi.routing import APIRouter
# from fastapi.security import OAuth2PasswordRequestForm

from schemas import users as user_schemas
from models import user as user_model
from database import get_session
from utils.encode_decode import create_access_token, get_password_hash, verify_password




router = APIRouter()


@router.post('/register/', response_model=user_schemas.UserDisplay)
def register_user(user: user_schemas.UserCreate, session: Session = Depends(get_session)):
    try:
        existing_user = session.query(user_model.User).filter_by(email=user.email).first()
        
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        encrypted_password = get_password_hash(user.password)
        new_user = user_model.User(
            first_name=user.first_name, 
            middle_name=user.middle_name, 
            last_name=user.last_name, 
            email=user.email, 
            password=encrypted_password
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e




@router.post("/login", response_model=user_schemas.Token)
def login(request: user_schemas.LoginSchema, session: Session = Depends(get_session)):
    try:
        user = session.query(user_model.User).filter(user_model.User.email == request.email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Email")

        hashed_password = user.password

        if not verify_password(request.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Incorrect Password"
            )
        
        access = create_access_token(data={"sub": user.email})
        token_db = user_model.TokenTable(user_id=user.id, access_token=access, status=True)
        session.add(token_db)
        session.commit()
        session.refresh(token_db)

        return token_db
    
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e
