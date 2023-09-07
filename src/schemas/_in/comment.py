from pydantic import BaseModel


class CommentCreateIn(BaseModel):
    content: str
    product_id: int
    like: int = 0
    dislike: int = 0
    is_published: bool = True

    class Config:
        orm_mode = True


class CommentIdIn(BaseModel):
    id: int
