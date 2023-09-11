from datetime import datetime

import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from src.core.db.database import AsyncSession
from src.models.category import Category
from src.models.product import Product


class ProductController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_product(self, product_data):
        async with self.db_session:
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

    async def get_products_for_category(self, category_id):
        async with self.db_session:
            query = sa.select(Product).options(selectinload(
                Product.category)).join(Category).filter(Category.id == category_id)
            products = await self.db_session.execute(query)
            result = products.scalars().all()
            return result

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

    async def update_rating(self, product_id, rate_value):
        product = await self.get_product(product_id=product_id)
        async with self.db_session:
            product.total_rating += rate_value
            product.num_ratings += 1

            if product.num_ratings > 0:
                product.rate = product.total_rating / product.num_ratings
            else:
                product.rate = 0

            await self.db_session.commit()


class SortProduct:

    def __init__(self, products):
        self.products = products

    async def sort_by_price_cheap(self):
        sorted_products = sorted(
            self.products,
            key=lambda product: product.get("price", 0)
        )
        return sorted_products

    async def sort_by_price_expansive(self):
        sorted_products = sorted(
            self.products,
            key=lambda product: product.get("price", 0),
            reverse=True
        )
        return sorted_products

    async def sort_by_bestselling(self):
        sorted_products = sorted(
            self.products,
            key=lambda product: product.get("sole_amount", 0),
            reverse=True
        )
        return sorted_products

    async def sort_by_newest(self):
        sorted_products = sorted(
            self.products,
            key=lambda product: datetime.strptime(product.get('created_at'), '%Y-%m-%d %H:%M:%S.%f') if product.get(
                'created_at') else None,
            reverse=True)
        return sorted_products

    async def sort_by_rating(self):
        sorted_products = sorted(
            self.products,
            key=lambda product: product["rate"] if product["rate"] is not None else 0.0,
            reverse=True
        )
        return sorted_products
