from pydantic import json
import sqlalchemy as sa
from sqlalchemy import String, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import SQLBase
from src.core.db.mixins import UUIDMixin, IdMixin, TimestampMixin
from src.core.db.database import AsyncSession


class Product(SQLBase, UUIDMixin, IdMixin, TimestampMixin):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    attributes: Mapped[json] = mapped_column(JSON, nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")
    # comments = relationship("Comment", back_populates="product")
    images: Mapped[str] = mapped_column(String, nullable=True)

    @staticmethod
    async def create_product(session, product_data):
        async with session:
            new_product = Product(
                title=product_data.title,
                description=product_data.description,
                price=product_data.price,
                attributes=product_data.attributes,
                category_id=product_data.category_id,
            )
            session.add(new_product)
            await session.commit()
            return new_product

    @staticmethod
    async def get_all_products(session: AsyncSession):
        async with session:
            result = await session.execute(sa.select(Product.title, Product.id))
            products = result.all()
            serialized_products = []
            for product_tuple in products:
                serialized_product = {
                    "id": product_tuple[1],
                    "title": product_tuple[0]
                }
                serialized_products.append(serialized_product)

            return serialized_products

    @staticmethod
    async def delete_product(session: AsyncSession, product_id):
        delete_product = sa.delete(Product).where(Product.id == product_id)
        async with session:
            await session.execute(delete_product)
            await session.commit()

    @staticmethod
    @staticmethod
    async def get_product_by_title():
        ...
