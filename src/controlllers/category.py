from fastapi import HTTPException

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from src.core.db.database import AsyncSession
from src.models.category import Category
from src.models.product import Product


class CategoryController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_category(self, category_data):
        async with self.db_session:
            new_category = Category(**category_data.dict())
            if new_category.parent_id:
                parent_category = await self.db_session.get(Category, new_category.parent_id)
                if not parent_category:
                    raise HTTPException(status_code=404, detail="Parent category not found")
                new_category.parent = parent_category
        self.db_session.add(new_category)
        await self.db_session.commit()
        return new_category

    async def delete_category(self, category_id):
        async with self.db_session:
            category = await self.db_session.execute(
                sa.select(Category).filter(Category.id == category_id)
            )
            category = category.scalar()
            if category:
                await self.db_session.delete(category)
                await self.db_session.commit()

    async def get_all_category(self):
        async with self.db_session:
            categories = (
                await self.db_session.execute(
                    sa.select(Category)
                    .options(selectinload(Category.subcategories))
                    .filter(Category.parent_id.is_(None))
                )
            ).scalars().all()

            return categories
