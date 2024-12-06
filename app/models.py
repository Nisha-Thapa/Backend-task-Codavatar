from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    virtual_phone_numbers = relationship("VirtualPhoneNumber", back_populates="owner")


class VirtualPhoneNumber(Base):
    __tablename__ = "virtual_phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="virtual_phone_numbers")


class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    virtual_phone_number_id = Column(Integer, ForeignKey("virtual_phone_numbers.id"))
    call_type = Column(String)  # "incoming" or "outgoing"
    duration = Column(Integer)  # Call duration in seconds
