import os
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from src.routers import auth, user, product, category, comment
from src.core.middlewares.session import SessionMiddleware
from src.core.middlewares.response_logger import ResponseLoggerMiddleware


def make_middleware() -> List[Middleware]:
    middleware = [Middleware(ResponseLoggerMiddleware), Middleware(SessionMiddleware)]
    return middleware


app = FastAPI(debug=True, middleware=make_middleware())
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(comment.router)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "https://daniemarket.iran.liara.run",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-CSRF-TOKEN"]
)

dotenv_path = os.path.join(os.path.dirname(__file__), "core", ".env")
load_dotenv(dotenv_path)


@app.get("/get")
async def start():
    return {"message": "hello world"}


@app.post("/store")
async def store_data(key: str, value: str):
    return {"message": "Data stored in Redis"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
