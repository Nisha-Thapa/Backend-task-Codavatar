from sqlalchemy import (
    Column,
    Enum,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from src.app.core.database.data_connector import Base
from src.app.common.models import TimeStampMixin
from src.app.telephone.choices import CallType
from src.app.users.models import User  # noqa: F401


class VirtualPhoneNumber(Base, TimeStampMixin):
    __tablename__ = "virtual_phone_numbers"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="virtual_phone_numbers")
    call_logs = relationship("CallLog", back_populates="phone_number")


class CallLog(Base, TimeStampMixin):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True, index=True)
    phone_number_id = Column(
        Integer, ForeignKey("virtual_phone_numbers.id"), nullable=False
    )
    destination_phone_number = Column(String, nullable=False)
    call_start_time = Column(DateTime, default=func.now())
    call_duration_seconds = Column(Integer, nullable=False)
    direction = Column(Enum(CallType))

    phone_number = relationship("VirtualPhoneNumber", back_populates="call_logs")
