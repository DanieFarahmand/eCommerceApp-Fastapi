from typing import Optional, List

from pydantic import BaseModel


class CategoryCreateIn(BaseModel):
    name: str
    parent_id: Optional[int] = None


class DeleteCategoryIn(BaseModel):
    id: int


class CategoryIDIn(BaseModel):
    id: int
