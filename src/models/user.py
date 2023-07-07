from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Enum

from src.core.db.base import SQLBase
from src.core.db.mixins import UUIDMixin, IdMixin, TimestampMixin
from src.models.enums import UserRoleEnum


class User(SQLBase, UUIDMixin, IdMixin, TimestampMixin):
    __tablename__ = "users"

    firstname: Mapped[Optional[str]] = mapped_column(String(38), nullable=True)
    lastname: Mapped[Optional[str]] = mapped_column(String(38), nullable=True)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(8))
    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum),
        default_factory=UserRoleEnum.customer.value,
        nullable=False
    )

    @validates("email")
    def validate_email(self, value):
        if not value and not self.phone:
            raise ValueError("Either email or phone_number must be provided.")
        return value

    @validates("phone")
    def validate_phone(self, value):
        if not value and not self.email:
            raise ValueError("Either email or phone_number must be provided.")
        return value
