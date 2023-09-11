import datetime
from typing import List

from pydantic import BaseModel


class CommentOut(BaseModel):
    content: str
    reviewer_id: int
    product_id: int
    like: int
    dislike: int
    is_published: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class CommentsOut(BaseModel):
    comment_list: List[CommentOut]

    @staticmethod
    def serialize_comments(comments):
        comment_list = [CommentOut.from_orm(comment) for comment in comments]
        return CommentsOut(products_list=comment_list)

    class Config:
        orm_mode = True
