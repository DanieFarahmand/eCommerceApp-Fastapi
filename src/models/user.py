from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    comments_reviewed = relationship("Comment", back_populates="reviewer", cascade="all, delete-orphan")
