import datetime

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
