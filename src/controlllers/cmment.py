from src.core.db.database import AsyncSession
from src.models.comment import Comment


class CommentController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, comment_data):
        async with self.db_session:
            new_comment = Comment(
                content=comment_data.content,
                reviewer_id=comment_data.reviewer_id,
                product_id=comment_data.product_id,
                like=comment_data.like,
                dislike=comment_data.dislike
            )
            self.db_session.add(new_comment)
            await self.db_session.commit()
