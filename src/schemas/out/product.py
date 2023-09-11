import datetime
from typing import List, Optional

from pydantic import BaseModel


class ProductOut(BaseModel):
    title: str
    description: str
    price: int
    sold_amount: Optional[int]
    created_at: datetime.datetime
    rate: Optional[float]

    class Config:
        orm_mode = True


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
