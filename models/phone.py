import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func, Boolean, BigInteger
from sqlalchemy.orm import relationship


from database import Base


class VirtualPhoneNumber(Base):
    __tablename__ = 'virtual_phone_numbers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    phone_number = Column(BigInteger)

    user = relationship('User', back_populates='phone_numbers')
    call_logs = relationship('CallLog', back_populates='phone_number', cascade='all, delete-orphan')



class CallLog(Base):
    __tablename__ = 'call_logs'

    id = Column(Integer, primary_key=True)
    phone_id = Column(Integer, ForeignKey('virtual_phone_numbers.id'))
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, default=func.now(), onupdate=func.now())

    phone_number = relationship('VirtualPhoneNumber', back_populates='call_logs')
