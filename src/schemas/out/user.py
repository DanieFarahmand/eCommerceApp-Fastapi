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

    @staticmethod
    def serialize_users(users):
        user_list = [UserOut.from_orm(user) for user in users]
        return UsersOut(products_list=user_list)

    class Config:
        orm_mode = True
