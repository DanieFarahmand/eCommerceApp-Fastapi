# from sqlalchemy import String, Integer, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.core.db.base import SQLBase
# from src.core.db.mixins import IdMixin, TimestampMixin
# from src.models.user import User
# from src.models.product import Product
#
#
# class Comment(SQLBase, IdMixin, TimestampMixin):
#     __tablename__ = "comments"
#
#     content: Mapped[str] = mapped_column(String, nullable=False)
#     reviewer: Mapped[User] = relationship("User", backref="comments")
#     reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
#     product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
#     product: Mapped[Product] = relationship("Product", back_populates="comments")
#     like: Mapped[int] = mapped_column(Integer)
#     dislike: Mapped[int] = mapped_column(Integer)
