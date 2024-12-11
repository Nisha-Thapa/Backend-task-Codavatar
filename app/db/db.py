from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app.models import User, VirtualPhoneNumber, CallLog

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a Session class that will allow you to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables (if not already created) - This will create all models defined in your app
def create_db():
    # The engine will create the tables from the models
    User.metadata.create_all(bind=engine)
    VirtualPhoneNumber.metadata.create_all(bind=engine)
    CallLog.metadata.create_all(bind=engine)

# Dependency to get the database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
