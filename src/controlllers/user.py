from abc import ABC

from fastapi import Request, HTTPException, Depends

from src.core.db.database import AsyncSession
from src.core.exceptions import UserNotFoundException
from src.models.enums import UserRoleEnum
from src.models.user import User
from src.dependencies.auth_dependenies import get_current_user_from_db


class AbstractBaseUser(ABC):
    ...


class AdminUser(AbstractBaseUser):
    @staticmethod
    async def get_all_users(db_session: AsyncSession):
        return await User.get_all_users(session=db_session)

    @staticmethod
    async def get_user_by_id(user_id: int, db_session: AsyncSession):
        user = await User.get_user_by_id(session=db_session, user_id=user_id)
        if not user:
            raise UserNotFoundException("User with this id does not exist.")
        return user

    @staticmethod
    async def change_user_role(role: UserRoleEnum, user_id, db_session: AsyncSession):
        updated_user = await User.change_user_role(
            user_id=user_id,
            session=db_session,
            role=role,
        )
        return updated_user

    @staticmethod
    async def delete_user(user_id: int, db_session):
        await User.delete_user(session=db_session, user_id=user_id)


async def admin_access(user: User = Depends(get_current_user_from_db)):
    print(user.role.name)
    if user.role.name != "admin":
        raise HTTPException(403, "Forbidden")


async def customer_access(user: User):
    if user.role.name != "customer":
        raise HTTPException(403, "Forbidden")
