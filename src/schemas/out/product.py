from typing import List

from pydantic import BaseModel

from src.schemas.out.comment import CommentOut


class ProductOut(BaseModel):
    title: str
    description: str
    price: int

    class Config:
        orm_mode = True


class ProductCommentsOut(BaseModel):
    comment_list: List[CommentOut]

    class Config:
        orm_mode = True
