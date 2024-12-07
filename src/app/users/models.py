from sqlalchemy import (
    Column,
    Enum,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from src.app.core.database.data_connector import Base
from src.app.common.models import TimeStampMixin
from src.app.users.choices import Genders

# from src.app.telephone.models import VirtualPhoneNumber


class User(Base, TimeStampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    address = Column(String)
    gender = Column(Enum(Genders))

    virtual_phone_numbers = relationship(
        "VirtualPhoneNumber", back_populates="owner", cascade="all, delete"
    )
