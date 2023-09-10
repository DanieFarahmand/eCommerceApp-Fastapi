from typing import Union

import aioredis
from aioredis import Redis
from src.core.config import settings
from src.core.serializers import custom_json_dump, custom_json_load


class RedisHandler:
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.redis: Union[Redis, None] = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def get(self, name):
        try:
            serialized_name = custom_json_dump(name)
            result = await self.redis.get(serialized_name)
            if result:
                return custom_json_load(result)
        except aioredis.RedisError as e:
            raise ValueError(f"Failed to get the value from Redis: {e}")
        return None

    async def set(self, name, value, exp: int):
        try:
            serialized_name = custom_json_dump(name)
            serialized_value = custom_json_dump(value)
            return await self.redis.set(serialized_name, serialized_value, exp)
        except aioredis.RedisError as e:
            raise ValueError(f"Failed to set the value in Redis: {e}")

    async def delete(self, name):
        try:
            serialized_name = custom_json_dump(name)
            await self.redis.delete(serialized_name)
        except aioredis.RedisError as e:
            raise ValueError(f"Failed to delete the value from Redis: {e}")

    async def get_keys(self, pattern):
        keys = await self.redis.keys(pattern + "*")
        return keys


async def get_redis():
    redis_handler = RedisHandler()
    await redis_handler.connect()
    return redis_handler
