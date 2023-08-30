from typing import List

from pydantic import BaseModel

from src.models.enums import UserRoleEnum


class UserOut(BaseModel):
    id: int
    email: str
    role: UserRoleEnum

    class Config:
        orm_mode = True


class UsersOut(BaseModel):
    users: List[UserOut]

    class Config:
        orm_mode = True
