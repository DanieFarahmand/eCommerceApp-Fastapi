from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.controlllers.auth import AuthController
from src.core.db.database import AsyncSession, get_session

router = APIRouter(tags=["User"])


class UserRequest(BaseModel):
    phone: str


@router.post('/user/')
async def create_user_endpoint(user_data: UserRequest, session: AsyncSession = Depends(get_session)):
    user = await AuthController(db_session=session).register(user=user_data)
    return user

#
# @router.get("/users")
# async def get_all_users(session: AsyncSession = Depends(get_session)):
#     async with session() as async_session:
#         users = await User.get_all_users(async_session)
#     return [users]
