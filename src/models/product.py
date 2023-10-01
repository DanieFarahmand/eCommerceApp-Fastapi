from pydantic import json
from sqlalchemy import String, Integer, JSON, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import SQLBase
from src.core.db.mixins import IdMixin, TimestampMixin


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
    rate: Mapped[float] = mapped_column(Float, nullable=True)
    total_rating: Mapped[float] = mapped_column(Float, default=0)
    num_ratings: Mapped[int] = mapped_column(Integer, default=0)
    on_discount: Mapped[bool] = mapped_column(Boolean, default=False)
    discounted_price: Mapped[int] = mapped_column(Integer, nullable=True)
    discounts = relationship("Discount", back_populates="product")
