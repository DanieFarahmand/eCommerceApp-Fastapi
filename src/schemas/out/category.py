from typing import List

from pydantic import BaseModel

from src.schemas.out.product import ProductOut


class ProductsOut(BaseModel):
    products_list: List[ProductOut]

    class Config:
        orm_mode = True
