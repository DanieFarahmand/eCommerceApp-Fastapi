import sqlalchemy as sa
from fastapi import HTTPException
from starlette import status

from src.core.db.database import AsyncSession
from src.models.comment import Comment


class CommentController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, comment_data, user_id):
        async with self.db_session:
            new_comment = Comment(
                content=comment_data.content,
                reviewer_id=user_id,
                product_id=comment_data.product_id,
                like=comment_data.like,
                dislike=comment_data.dislike,
                is_published=comment_data.is_published
            )
            self.db_session.add(new_comment)
            await self.db_session.commit()

    async def delete(self, user_id, user_role, comment_id):
        async with self.db_session:
            await self.db_session.execute(
                sa.delete(Comment)
                .where(Comment.id == comment_id)
                .where(sa.or_(user_role == "admin", Comment.reviewer_id == user_id))
                .returning(Comment)
            )
            await self.db_session.commit()

    async def add_to_like(self, comment_id):
        async with self.db_session:
            comment = await self.db_session.get(Comment, comment_id)
            if comment is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            comment.like += 1
            await self.db_session.commit()
            return comment

    async def add_to_dislike(self, comment_id):
        async with self.db_session:
            comment = await self.db_session.get(Comment, comment_id)
            if comment is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )
            comment.dislike += 1
            await self.db_session.commit()
            return comment

    async def publish(self, comment_id):
        async with self.db_session:
            comment = await self.db_session.get(Comment, comment_id)
            if comment is None:
                raise HTTPException(status_code=404, detail="Comment not found.")
            if comment.is_published:
                raise HTTPException(status_code=400, detail="comment is already published.")
            comment.is_published = True
            await self.db_session.commit()
            return comment
