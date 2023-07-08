from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.models.user import User


class AuthController:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def register(self, user):
        user = select(User).where(User.id == user["id"])
        if user is None:
            async with self.db_session as session:
                user = insert(User)

    def login(self):
        ...

    def logout(self):
        ...
