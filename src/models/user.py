from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Enum
# from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.base import SQLBase
from src.core.db.database import async_engine, AsyncSession
from src.core.db.mixins import UUIDMixin, IdMixin, TimestampMixin
from src.models.enums import UserRoleEnum
from src.utils.password import PasswordHandler
from src.core.exceptions import UserAlreadyExistsException


class User(SQLBase, UUIDMixin, IdMixin, TimestampMixin):
    __tablename__ = "users"

    firstname: Mapped[Optional[str]] = mapped_column(String(38), nullable=True)
    lastname: Mapped[Optional[str]] = mapped_column(String(38), nullable=True)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=True, index=True)
    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=True, index=True)
    password: Mapped[str] = mapped_column(String(8))
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum),
        default=UserRoleEnum.customer.value,
        nullable=False,
    )

    @validates("email")
    def validate_email(self, key, value):
        if not value and not self.phone:
            raise ValueError("Either email or phone_number must be provided.")
        return value

    @validates("phone")
    def validate_phone(self, key, value):
        if not value and not self.email:
            raise ValueError("Either email or phone_number must be provided.")
        return value

    @staticmethod
    async def create_user_by_email(session: AsyncSession, email, password):
        get_user = sa.select(User).where(email == User.email)
        existing_user = await session.scalar(get_user)
        if existing_user is not None:
            raise UserAlreadyExistsException(
                message="User with this email already exists.")
        async with session:
            new_user = User(
                email=email,
                password=PasswordHandler.hash(password),
            )
            session.add(new_user)
            await session.commit()
        return new_user

    @staticmethod
    async def create_user_by_phone(session: AsyncSession, phone, password):
        get_user = sa.select(User).where(phone == User.phone)
        existing_user = await session.scalar(get_user)
        if existing_user is not None:
            raise UserAlreadyExistsException(
                message="User with this phone number already exists.")
        new_user = User(
            email=phone,
            password=PasswordHandler.hash(password),
        )
        async with session:
            session.add(new_user)
            await session.commit()
        return new_user

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        return await session.get(User, user_id)

    @staticmethod
    async def get_all_users(session: AsyncSession):
        return await session.execute(sa.select(User))

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str):
        return await session.execute(sa.select(User).where(User.email == email))

    @staticmethod
    async def get_user_by_phone(session: AsyncSession, phone: str):
        return await session.execute(sa.select(User).where(User.phone == phone))
