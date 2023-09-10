from pydantic import json
from sqlalchemy import String, Integer, JSON, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import SQLBase
from src.core.db.mixins import IdMixin, TimestampMixin
from src.models.enums import ProductRatingEnum


class Product(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    attributes: Mapped[json] = mapped_column(JSON, nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id', ondelete="CASCADE"))
    category = relationship("Category", back_populates="products")
    comments = relationship("Comment", back_populates="product", cascade="all, delete-orphan")
    images: Mapped[str] = mapped_column(String, nullable=True)
    sold_amount: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[ProductRatingEnum] = mapped_column(Enum(ProductRatingEnum), nullable=True)
