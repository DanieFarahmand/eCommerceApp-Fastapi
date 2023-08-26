from pydantic import BaseModel, EmailStr, EmailError, Field, validator

from src.models.enums import UserRoleEnum


class ChangeRoleIn(BaseModel):
    role: UserRoleEnum
