import os

from dotenv import load_dotenv
from fastapi import FastAPI

from src.routers import user
from src.core.redis import RedisHandler

redis_handler = RedisHandler()

dotenv_path = os.path.join(os.path.dirname(__file__), "core", ".env")
load_dotenv(dotenv_path)

app = FastAPI(debug=True)
app.include_router(user.router)


@app.on_event("startup")
async def startup():
    await redis_handler.connect()


@app.on_event("shutdown")
async def shutdown():
    await redis_handler.disconnect()


@app.get("/get")
async def start():
    data = await redis_handler.get("my_key")
    return {"message": "hello world", "data_from_redis": data}


@app.get("/store")
async def store_data():
    key = "my_key"
    value = "my_value"
    exp = 3600  # Expiration time in seconds
    await redis_handler.set(key, value, exp)
    return {"message": "Data stored in Redis"}
