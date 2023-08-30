from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str
    reviewer_id: int
    product_id: int
    like: int = 0
    dislike: int = 0

    class Config:
        orm_mode = True
