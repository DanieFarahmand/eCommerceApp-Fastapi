from pydantic import BaseModel

from src.models.enums import UserRoleEnum


class ChangeRoleIn(BaseModel):
    role: UserRoleEnum


class UserIdIn(BaseModel):
    id: int
