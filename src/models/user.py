from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum

from src.core.db.base import SQLBase
from src.core.db.database import AsyncSession
from src.core.db.mixins import UUIDMixin, IdMixin, TimestampMixin
from src.models.enums import UserRoleEnum
from src.utils.password import PasswordHandler
from src.core.exceptions import UserAlreadyExistsException


class User(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "users"

    firstname: Mapped[Optional[str]] = mapped_column(String(38), nullable=True)
    lastname: Mapped[Optional[str]] = mapped_column(String(38), nullable=True)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=True, index=True)
    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=True, index=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum),
        default=UserRoleEnum.customer.value,
        nullable=False,
    )

    @staticmethod
    async def create_user(session: AsyncSession, email, password, phone):
        user = sa.select(User).where(sa.and_(User.email == email, User.phone == phone))
        existing_user = await session.scalar(user)
        if existing_user is not None:
            raise UserAlreadyExistsException(
                message="User with this email already exists.")
        async with session:
            new_user = User(
                phone=phone,
                email=email,
                password=PasswordHandler.hash(password),
            )
            session.add(new_user)
            await session.commit()
        return new_user

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        result = await session.execute(sa.select(User).where(User.id == user_id))
        user = result.scalar()
        return user

    @staticmethod
    async def get_all_users(session: AsyncSession):
        return await session.execute(sa.select(User))

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str):
        result = await session.execute(sa.select(User).where(User.email == email))
        user = result.scalar()
        return user

    @staticmethod
    async def get_user_by_phone(session: AsyncSession, phone: str):
        result = await session.execute(sa.select(User).where(User.phone == phone))
        user = result.scalar()
        return user

    @staticmethod
    async def change_user_role(session: AsyncSession, user_id, role: UserRoleEnum):
        async with session:
            updated_user = await session.execute(
                sa.update(User).where(User.id == user_id).values(role=role).returning(User))
            updated_user = updated_user.fetchone()
            await session.commit()
            return updated_user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int):
        delete_query = sa.delete(User).where(User.id == user_id)
        async with session:
            await session.execute(delete_query)
            await session.commit()
