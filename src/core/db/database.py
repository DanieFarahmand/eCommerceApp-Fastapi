# import logging
# from typing import AsyncIterator
#
# from fastapi import Depends
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
#
# from src.core.config import settings
#
# logger = logging.getLogger(__name__)
#
# async_engine = create_async_engine(
#     settings.DATABASE_URL,
#     pool_pre_ping=True,
#     echo=settings.ECHO_SQL,
# )
# AsyncSessionLocal = async_sessionmaker(
#     bind=async_engine,
#     autoflush=False,
#     future=True,
# )
#
#
# async def get_session() -> AsyncIterator[async_sessionmaker]:
#     try:
#         yield AsyncSessionLocal
#     except SQLAlchemyError as e:
#         logger.exception(e)
#
#
# AsyncSession = Depends(get_session)
from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.config import settings

async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ECHO_SQL,
)

async_session = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            # Handle any exception if needed
            raise e


AsyncSession = Depends(get_session)
