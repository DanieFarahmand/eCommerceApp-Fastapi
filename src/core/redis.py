from typing import Union
import json

import aioredis
from aioredis import Redis
from src.core.config import settings


class RedisHandler:
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.redis: Union[Redis, None] = None

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
        try:
            serialized_name = await self.serialize(name)
            result = await self.redis.get(serialized_name)
            if result:
                return await self.deserialize(result)
        except aioredis.RedisError as e:
            raise ValueError(f"Failed to get the value from Redis:{e}")
        return None

    async def set(self, name, value, exp: int):
        try:
            serialized_name = await self.serialize(name)
            serialized_value = await self.serialize(value)
            return await self.redis.set(serialized_name, serialized_value, exp)
        except aioredis.RedisError as e:
            raise ValueError(f"Failed to set the value in Redis:{e}")

    async def delete(self, name):
        try:
            serialized_name = await self.serialize(name)
            await self.redis.delete(serialized_name)
        except aioredis.RedisError as e:
            raise ValueError(f"Failed to delete the value from Redis:{e}")
