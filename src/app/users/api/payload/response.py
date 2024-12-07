from pydantic import BaseModel

from src.app.users.choices import Genders


class User(BaseModel):
    id: int | None
    name: str | None
    email: str | None
    address: str | None
    gender: Genders | None

    class Config:
        from_attributes = True


class UserList(BaseModel):
    users: list[User]
