from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    virtual_phone_numbers = relationship("VirtualPhoneNumber", back_populates="owner")

class VirtualPhoneNumber(Base):
    __tablename__ = "virtual_phone_numbers"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(15), unique=True, nullable=False) #Enfocring the number to be under 15
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="virtual_phone_numbers")

class CallLog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True, index=True)
    from_number = Column(String, nullable=False)
    to_number = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
