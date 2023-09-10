from datetime import datetime

import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.orm import joinedload, selectinload

from src.core.db.database import AsyncSession
from src.models.product import Product


class ProductController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_product(self, product_data):
        async with   self.db_session:
            new_product = Product(
                title=product_data.title,
                description=product_data.description,
                price=product_data.price,
                attributes=product_data.attributes,
                category_id=product_data.category_id,
            )
            self.db_session.add(new_product)
            await self.db_session.commit()
            return new_product

    async def get_product(self, product_id):
        async with self.db_session.begin():
            result = await self.db_session.execute(sa.select(Product).where(Product.id == product_id))
            product = result.scalar()
            if product is None:
                raise HTTPException(status_code=404, detail="product not found")
            return product

    async def get_all_products(self):
        async with self.db_session:
            products = await self.db_session.execute(
                sa.select(Product)
            )
            return products.scalars().all()

    async def delete_product(self, product_id):
        async with self.db_session:
            product = await self.db_session.execute(
                sa.select(Product).filter(Product.id == product_id)
            )
            product = product.scalar()
            if not product:
                raise HTTPException(status_code=404, detail="product not found")

            await self.db_session.delete(product)
            await self.db_session.commit()

    async def get_comments(self, product_id):
        async with self.db_session as session:
            query = (
                sa.select(Product)
                .filter(Product.id == product_id)
                .options(selectinload(Product.comments))
            )
            product = await session.execute(query)
            product = product.scalar()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found.")
            comments = product.comments
            return comments

    async def product_rate_average(self, product_id):
        product = self.get_product(product_id=product_id)

    @staticmethod
    async def sort_by_price_cheap(products):
        sorted_products = sorted(
            products,
            key=lambda product: product.get("price", 0)
        )
        return sorted_products

    @staticmethod
    async def sort_by_price_expansive(products):
        sorted_products = sorted(
            products,
            key=lambda product: product.get("price", 0),
            reverse=True
        )
        return sorted_products

    @staticmethod
    async def sort_by_bestselling(products):
        sorted_products = sorted(
            products,
            key=lambda product: product.get("sole_amount", 0),
            reverse=True
        )
        return sorted_products

    @staticmethod
    async def sort_by_newest(products):
        sorted_products = sorted(
            products,
            key=lambda product: datetime.strptime(product.get('created_at'), '%Y-%m-%d %H:%M:%S.%f') if product.get(
                'created_at') else None,
            reverse=True)
        return sorted_products

    @staticmethod
    async def sort_by_rating(products):
        ...
