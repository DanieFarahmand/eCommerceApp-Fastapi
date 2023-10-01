import asyncio
from datetime import datetime, timedelta

from fastapi import Depends
from rocketry import Rocketry
from rocketry.conds import every
import sqlalchemy as sa

from src.core.db.database import AsyncSession, get_session
from src.models.discount import Discount

app = Rocketry(config={"task_execution": "async"})


@app.task(every('10 seconds', based="finish"))
async def expire_discounts(db_session: AsyncSession):
    async with db_session:
        print("sdjkl;hfal gbfvipahsdf;ioah")
        expiration_threshold = datetime.utcnow() - timedelta(seconds=10)

        expired_discounts = await db_session.execute(
            sa.select(Discount).filter(Discount.created_at <= expiration_threshold)
        )
        expired_discounts = expired_discounts.scalars().all()
        for discount in expired_discounts:
            discount.expired = True

        await db_session.commit()


if __name__ == "__main__":
    # Run only Rocketry
    app.run()
