from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./cloud_telephony.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()