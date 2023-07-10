from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.models.user import User
from src.core.db.database import AsyncSession
from src.utils.jwt import JWTHandler


class AuthController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def register(self, user):
        new_user = await User.create_user_by_email(
            email=user.email, password=user.password, session=self.db_session
        )
        return new_user

    def login(self):
        ...

    def logout(self):
        ...
