from fastapi import APIRouter, Depends, HTTPException

from src.core.db.database import get_session, AsyncSession
from src.dependencies.user_dependencies import admin_access
from src.models.user import User
from src.schemas._in.comment import CommentCreateIn, CommentIdIn
from src.controlllers.cmment import CommentController
from src.dependencies.auth_dependenies import get_current_user_from_db

router = APIRouter(prefix="/comment", tags=["Comments"])


@router.post("/", dependencies=[])
async def create_comment(
        comment_data: CommentCreateIn,
        db_session: AsyncSession = Depends(get_session),
        user: User = Depends(get_current_user_from_db)):
    await CommentController(db_session=db_session).create(
        comment_data=comment_data,
        user_id=user.id
    )
    return {"message": "Your comment added."}


@router.delete("/")
async def delete_comment(
        comment_id: CommentIdIn,
        user: User = Depends(get_current_user_from_db),
        db_session: AsyncSession = Depends(get_session)):
    await CommentController(db_session=db_session).delete(
        comment_id=comment_id.id,
        user_id=user.id,
        user_role=user.role.name
    )


@router.put("/like")
async def like_comment(
        comment_id: CommentIdIn,
        db_session: AsyncSession = Depends(get_session)):
    comment = await CommentController(db_session=db_session).add_to_like(comment_id=comment_id.id)
    if comment:
        return {"message": "a like added for this comment"}
    else:
        raise HTTPException(status_code=404, detail="comment not found.")


@router.put("/dislike")
async def dislike_comment(
        comment_id: CommentIdIn,
        db_session: AsyncSession = Depends(get_session)):
    comment = await CommentController(db_session=db_session).add_to_dislike(comment_id=comment_id.id)
    if comment:
        return {"message": "a dislike added for this comment."}
    else:
        raise HTTPException(status_code=404, detail="comment not found.")


@router.put("/publish", dependencies=[Depends(admin_access)])
async def publish_comment(comment_id: CommentIdIn, db_session: AsyncSession = Depends(get_session)):
    comment = await CommentController(db_session=db_session).publish(comment_id=comment_id)
    if comment:
        return {"message": "comment published."}



