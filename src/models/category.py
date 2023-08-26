from fastapi import HTTPException

import sqlalchemy as sa
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from src.core.db.base import SQLBase
from src.core.db.database import AsyncSession
from src.core.db.mixins import IdMixin


class Category(SQLBase, IdMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String, index=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    subcategories = relationship("Category", back_populates="parent", remote_side="Category.parent_id")
    parent = relationship("Category", back_populates="subcategories", remote_side="Category.id")
    products = relationship("Product", back_populates="category")

    @staticmethod
    async def create_category(session: AsyncSession, category_data):
        async with session.begin():
            new_category = Category(**category_data.dict())
            if new_category.parent_id:
                parent_category = await session.get(Category, new_category.parent_id)
                if not parent_category:
                    raise HTTPException(status_code=404, detail="Parent category not found")
                new_category.parent = parent_category
        session.add(new_category)
        await session.commit()
        return new_category

    @staticmethod
    async def delete_category(session: AsyncSession, category_id):
        delete_category = sa.delete(Category).where(Category.id == category_id)
        async with session:
            await session.execute(delete_category)
            await session.commit()

    @staticmethod
    async def get_all_category(session: AsyncSession):
        async with session:
            categories = (
                await session.execute(
                    sa.select(Category)
                    .options(selectinload(Category.subcategories))
                    .filter(Category.parent_id.is_(None))
                )
            ).scalars().all()

            return categories

    @staticmethod
    async def get_category_products():
        ...
