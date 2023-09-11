from typing import List

from pydantic import BaseModel

from src.schemas.out.product import ProductOut


class ProductsOut(BaseModel):
    products_list: List[ProductOut]

    @staticmethod
    def serialize_products_from_redis(products):
        products_list = [ProductOut.parse_obj(product) for product in products]
        return ProductsOut(products_list=products_list)

    @staticmethod
    def serialize_products(products):
        products_list = [ProductOut.from_orm(product) for product in products]
        return ProductsOut(products_list=products_list)

    class Config:
        orm_mode = True
