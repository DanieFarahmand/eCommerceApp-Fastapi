from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum

from src.core.db.base import SQLBase
from src.core.db.mixins import IdMixin, TimestampMixin
from src.models.enums import UserRoleEnum


class User(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=True, index=True)

    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum),
        default=UserRoleEnum.customer.value,
        nullable=False,
    )
    comments_reviewed = relationship("Comment", backref="reviewer",
                                     cascade="all, delete-orphan")
