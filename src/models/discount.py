from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import SQLBase
from src.core.db.mixins import IdMixin, TimestampMixin


class DiscountCouponBase(SQLBase, IdMixin, TimestampMixin):
    __abstract__ = True

    discount_percent: Mapped[int] = mapped_column(Integer, nullable=True)
    expired: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expiration_hours: Mapped[int] = mapped_column(Integer, nullable=False)


class Discount(DiscountCouponBase):
    __tablename__ = "discounts"

    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="discounts")


class Coupon(DiscountCouponBase):
    __tablename__ = "coupons"

    code: Mapped[str] = mapped_column(String(20), nullable=False)
