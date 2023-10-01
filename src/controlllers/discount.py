from datetime import timedelta, datetime

import sqlalchemy as sa
from fastapi import HTTPException

from src.core.db.database import AsyncSession
from src.models.discount import Coupon, Discount
from src.models.product import Product


class CouponController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def generate_coupon(self, code_name, discount_percent, expiration_hours):
        async with self.db_session:
            new_coupon = Coupon(
                code=code_name,
                discount_percent=discount_percent,
                expiration_hours=expiration_hours,
                expired=False,
            )
            self.db_session.add(new_coupon)
            await self.db_session.commit()

            return new_coupon.code

    async def use_coupon(self, code, total_price):
        async with self.db_session:
            coupon = await self.db_session.execute(sa.select(Coupon).where(Coupon.code == code))
            coupon = coupon.scalar()
            coupon_expiration_date = coupon.created_at + timedelta(hours=coupon.expiration_hours)
            if datetime.utcnow() >= coupon_expiration_date:
                raise HTTPException(status_code=404, detail="Coupon is expired")

            new_price = total_price * (coupon.discount_percent / 100)
            await self.db_session.commit()
            return new_price


class DiscountController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def apply(self, discount_percent, expiration_hours, product_id):
        product = await self.db_session.execute(sa.select(Product).where(Product.id == product_id))
        product = product.scalar()

        async with self.db_session:
            new_discount = Discount(
                discount_percent=discount_percent,
                expired=False,
                expiration_hours=expiration_hours,
                product_id=product_id
            )
            product.on_discount = True
            product.discounted_price = product.price * (discount_percent / 100)

            self.db_session.add(new_discount)
            await self.db_session.commit()

            return new_discount.id

    async def delete(self, discount_id):
        async with self.db_session:
            discount = await self.db_session.execute(
                sa.select(Discount).filter(Discount.id == discount_id)
            )
            discount = discount.scalar()
            if not discount:
                raise HTTPException(status_code=404, detail="product not found")

            await self.db_session.delete(discount)
            product = await self.db_session.execute(
                sa.select(Product).filter(Product.id == discount.product_id)
            )
            product = product.scalar()
            product.discounted_price = None
            product.on_discount = False
            await self.db_session.commit()

    async def delete_all_discounts(self):
        async with self.db_session:
            await self.db_session.execute(sa.delete(Discount))
            await self.db_session.commit()
