import asyncio

import sqlalchemy as sa
from fastapi import HTTPException

from src.core.db.database import AsyncSession
from src.models.discount import Discount
from src.models.product import Product
from src.schedulers.scheduler import app as app_rocketry


@app_rocketry.task(multilaunch=True)
async def expire_discount(discount_id, db_session: AsyncSession):
    async with db_session:
        discount = await db_session.execute(
            sa.select(Discount).filter(Discount.id == discount_id)
        )
        discount = discount.scalar()
        if not discount:
            raise HTTPException(status_code=404, detail="Discount not found")
        discount.expired = True

        product = await db_session.execute(
            sa.select(Product).filter(Product.id == discount.product_id)
        )
        product = product.scalar()
        product.discounted_price = None
        product.on_discount = False
        await db_session.commit()
