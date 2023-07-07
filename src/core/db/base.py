from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class SQLBase(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()
