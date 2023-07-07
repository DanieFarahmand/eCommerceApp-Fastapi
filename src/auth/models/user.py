# from pydantic import BaseModel
#
# from sqlalchemy.orm import Mapped, mapped_column, selectinload
# from sqlalchemy import String, Enum, select
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.core.db.base import SQLBase
# from src.core.db.mixins import IdMixin, TimestampMixin
# from src.auth.models.enum import UserRole
#
#
# class UserRequest(BaseModel):
#     firstname: str
#     lastname: str
#     phone_number: str
#     email: str
#
#
# class User(SQLBase, IdMixin, TimestampMixin):
#     __tablename__ = "users"
#     firstname: Mapped[str] = mapped_column(String(38), nullable=False)
#     lastname: Mapped[str] = mapped_column(String(38), nullable=False)
#     phone_number: Mapped[str] = mapped_column(String(10), nullable=False)
#     email: Mapped[str] = mapped_column(String(58), nullable=False)
#     role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.normal_user.value, nullable=False)
#
#     @classmethod
#     async def create_user(cls, session: AsyncSession, user_data: UserRequest):
#         user = User(
#             firstname=user_data.firstname,
#             lastname=user_data.lastname,
#             phone_number=user_data.phone_number,
#             email=user_data.email,
#             role=UserRole.normal_user
#         )
#         session.add(user)
#         await session.flush()
#         await session.commit()
#         return user
#
#     @classmethod
#     async def get_all_users(cls, session: AsyncSession):
#         query = select(cls)
#         result = await session.execute(query)
#         users = result.scalars().all()
#         return users
