from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas.user import UserCreate

from app.utils import hash_password  

# Create an APIRouter instance
router = APIRouter()


# Endpoint to create a user
@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the user's password
    hashed_password = hash_password(user.password)
    
    # Create a new user with the hashed password
    db_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  
    return db_user
