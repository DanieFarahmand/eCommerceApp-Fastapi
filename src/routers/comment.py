from fastapi import APIRouter, Depends

from src.core.db.database import get_session, AsyncSession
from src.schemas._in.comment import CommentCreate
from src.controlllers.cmment import CommentController
from src.dependencies.auth_dependenies import get_current_user_from_db

router = APIRouter(prefix="/comment", tags=["Comments"])


@router.post("/", dependencies=[Depends(get_current_user_from_db)])
async def create_comment(
        comment_data: CommentCreate,
        db_session: AsyncSession = Depends(get_session)):
    await CommentController(db_session=db_session).create(comment_data=comment_data)
    return {"message": "Your comment added."}
