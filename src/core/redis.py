import datetime
from typing import Union
import json

import aioredis
from aioredis import Redis
from src.core.config import settings


class RedisHandler:
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.redis: Union[None, Redis] = None

    @staticmethod
    async def serialize(value) -> str:
        return json.dumps(value)

    @staticmethod
    async def deserialize(serialized_value: str):
        return json.loads(serialized_value)

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def get(self, name):
        serialized_name = await self.serialize(name)
        result = await self.redis.get(serialized_name)
        if result:
            return await self.deserialize(result)

        return None

    async def set(self, name, value, exp: int):
        serialized_name = await self.serialize(name)
        serialized_value = await self.serialize(value)
        return await self.redis.set(serialized_name, serialized_value, exp)

    async def delete(self, name):
        serialized_name = await self.serialize(name)
        await self.redis.delete(serialized_name)
