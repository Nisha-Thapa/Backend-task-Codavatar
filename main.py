from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel


# Database setup
DATABASE_URL = "sqlite:///./test1.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a schema for the phone number
class PhoneNumberCreate(BaseModel):
    number: str
# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    virtual_phone_numbers = relationship("VirtualPhoneNumber", back_populates="owner")

class VirtualPhoneNumber(Base):
    __tablename__ = "virtual_phone_numbers"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="virtual_phone_numbers")

class CallLog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True, index=True)
    caller = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    virtual_phone_number_id = Column(Integer, ForeignKey("virtual_phone_numbers.id"))

# Create tables
Base.metadata.create_all(bind=engine)





# FastAPI app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/users/{user_id}/virtual-phone-numbers")
def get_virtual_phone_numbers(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        {"id": vp.id, "number": vp.number} for vp in user.virtual_phone_numbers
    ]



@app.on_event("startup")
def startup_data():
    db = SessionLocal()
    # Check if there are any users already
    if not db.query(User).count():
        user1 = User(name="Alice", email="alice@example.com")
        user2 = User(name="Bob", email="bob@example.com")
        db.add(user1)
        db.add(user2)
        db.commit()
    db.close()

@app.get("/debug/database/users")
def debug_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/users/{user_id}/virtual-phone-numbers")
def create_virtual_phone_number(
    user_id: int,
    phone_number: PhoneNumberCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate if the phone number already exists
    existing_number = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.number == phone_number.number).first()
    if existing_number:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    # Create a new virtual phone number
    new_number = VirtualPhoneNumber(number=phone_number.number, owner=user)
    db.add(new_number)
    db.commit()
    db.refresh(new_number)

    return {"id": new_number.id, "number": new_number.number}



