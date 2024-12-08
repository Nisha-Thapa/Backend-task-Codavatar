from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_numbers = relationship("VirtualPhoneNumber", back_populates="owner")

class VirtualPhoneNumber(Base):
    __tablename__ = "virtual_phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="phone_numbers")

class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    from_number = Column(String, nullable=False)
    to_number = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)
    virtual_phone_number_id = Column(Integer, ForeignKey("virtual_phone_numbers.id"))