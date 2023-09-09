from fastapi import HTTPException

from src.core.redis import RedisHandler


class CacheHandler:
    def __init__(self, redis_db: RedisHandler):
        self.redis_db = redis_db
        self.prefix = "cache/"

    async def get_cached_data(self, name):
        data = await self.redis_db.get(self.prefix + name)
        if not data:
            raise HTTPException(status_code=404, detail="data not found.")
        return data

    async def set_cached_data(self, name, value, exp):
        await self.redis_db.delete(name=self.prefix + name)
        await self.redis_db.set(name=self.prefix + name, value=value, exp=exp)

    async def clear_cache(self):
        keys_to_delete = await self.redis_db.get_keys(pattern=self.prefix)
        if keys_to_delete:
            await self.redis_db.delete(*keys_to_delete)

    async def get_or_set(self, name, value, exp):
        cached_data = await  self.get_cached_data(name=self.prefix + name)
        if not cached_data:
            await  self.set_cached_data(name=self.prefix + name, value=value, exp=exp)

    async def delete_cached_data(self, name):
        await self.redis_db.delete(name=self.prefix + name)
