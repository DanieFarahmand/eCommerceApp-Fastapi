from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import SQLBase
from src.core.db.mixins import IdMixin, TimestampMixin


class Comment(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(String)
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    reviewer = relationship("User", back_populates="comments_reviewed")
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    product = relationship("Product", back_populates="comments")
    like: Mapped[int] = mapped_column(Integer)
    dislike: Mapped[int] = mapped_column(Integer)
