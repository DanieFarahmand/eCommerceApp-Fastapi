# from fastapi import APIRouter, Depends
#
# from src.core.db.database import AsyncSession, get_session, AsyncSessionLocal
# from src.auth.models.user import User, UserRequest
#
# router = APIRouter(tags=["User"])
#
#
# @router.post('/user/')
# async def create_user_endpoint(user_data: UserRequest, session: AsyncSession = Depends(get_session)):
#     async with session() as async_session:
#         user = await User.create_user(async_session, user_data=user_data)
#         async_session.add(user)
#         await async_session.flush()
#         await async_session.refresh(user)
#         return user
#
#
# @router.get("/users")
# async def get_all_users(session: AsyncSession = Depends(get_session)):
#     async with session() as async_session:
#         users = await User.get_all_users(async_session)
#     return [users]
