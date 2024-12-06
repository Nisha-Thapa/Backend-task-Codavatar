from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime
import re

from sqlalchemy.types import DateTime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    virtual_phone_numbers = relationship("VirtualPhoneNumber", back_populates="owner")
    
        
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}'>"


class VirtualPhoneNumber(Base):
    __tablename__ = "virtual_phone_numbers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="virtual_phone_numbers")
    
    def __repr__(self):
        return f"<VirtualPhoneNumber(id={self.id}, number='{self.number}', user_id={self.user_id}>"


class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    virtual_phone_number_id = Column(Integer, ForeignKey("virtual_phone_numbers.id"))
    call_type = Column(String)  # "incoming" or "outgoing"
    duration = Column(Integer)  # Call duration in seconds
    
    def __repr__(self):
        return f"<CallLog(id={self.id}, virtual_phone_number_id={self.virtual_phone_number_id}, call_type='{self.call_type}', duration={self.duration})>"
