from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import SQLBase
from src.core.db.mixins import IdMixin


class Category(SQLBase, IdMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String, index=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), nullable=True)
    parent = relationship("Category", back_populates="subcategories", remote_side="Category.id")
    subcategories = relationship("Category", back_populates="parent", remote_side="Category.parent_id")
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
