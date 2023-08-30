from typing import Dict

from pydantic import BaseModel
from src.models.category import Category


class ProductCreateIn(BaseModel):
    title: str
    description: str
    price: int
    attributes: Dict
    category_id: int

    class Config:
        arbitrary_types_allowed = True


class ProductDeleteIn(BaseModel):
    id: int


class GetProductIn(BaseModel):
    id: int
