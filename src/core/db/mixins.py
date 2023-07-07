import uuid
import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, BigInteger, String


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class IdMixin:
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )


class UUIDMixin:
    uuid: Mapped[str] = mapped_column(
        String, primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )
