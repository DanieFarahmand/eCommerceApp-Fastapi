from fastapi import HTTPException, Depends
import sqlalchemy as sa
from src.core.db.database import AsyncSession
from src.core.exceptions import UserAlreadyExistsException
from src.models.enums import UserRoleEnum
from src.models.user import User
from src.dependencies.auth_dependenies import get_current_user_from_db


class UserController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, phone):
        user = sa.select(User).where(User.phone == phone)
        existing_user = await self.db_session.scalar(user)
        if existing_user is not None:
            raise UserAlreadyExistsException(
                message="User with this email already exists.")
        async with self.db_session:
            new_user = User(
                phone=phone,
            )
            self.db_session.add(new_user)
            await self.db_session.commit()
        return new_user

    async def get_user_by_id(self, user_id):
        result = await self.db_session.execute(sa.select(User).where(User.id == user_id))
        user = result.scalar()
        return user

    async def get_all_users(self):
        result = await self.db_session.execute(sa.select(User))
        users = result.scalars().all()
        return users

    async def get_user_by_email(self, email: str):
        result = await self.db_session.execute(sa.select(User).where(User.email == email))
        user = result.scalar()
        return user

    async def get_user_by_phone(self, phone: str):
        result = await self.db_session.execute(sa.select(User).where(User.phone == phone))
        user = result.scalar()
        return user

    async def change_user_role(self, user_id, role: UserRoleEnum):
        async with self.db_session:
            updated_user = await self.db_session.execute(
                sa.update(User).where(User.id == user_id).values(role=role).returning(User))
            updated_user = updated_user.fetchone()
            await self.db_session.commit()
            return updated_user

    async def delete_user(self, user_id):
        async with self.db_session:
            user = await self.db_session.execute(
                sa.select(User).filter(User.id == user_id)
            )
            user = user.scalar()
            if user:
                await self.db_session.delete(user)
                await self.db_session.commit()
