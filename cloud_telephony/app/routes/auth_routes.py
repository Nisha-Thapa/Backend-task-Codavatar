import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin, Token
from utils.auth_utils import hash_password, verify_password

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Password encryption context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    # Set token expiry for 1 hour
    expiration = datetime.utcnow() + timedelta(hours=1)
    token_data = {"sub": data["sub"], "exp": expiration}
    # Encode token using password hashing (you may replace with JWT implementation)
    token = pwd_context.hash(str(token_data))
    return token


# Dependency for database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User Registration
@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("Register endpoint called.")
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.error(f"Username already exists: {user.username}")
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": user.username})
    logger.info(f"User {user.username} successfully registered.")
    return {"access_token": token, "token_type": "bearer"}


# User Login
@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    logger.info("Login endpoint called.")
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logger.error("Invalid username or password.")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})
    logger.info(f"User {user.username} successfully logged in.")
    return {"access_token": token, "token_type": "bearer"}
