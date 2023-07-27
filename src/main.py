import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth
from src.core.middlewares.session import SessionMiddleware
from src.core.middlewares.response_logger import ResponseLoggerMiddleware

app = FastAPI(debug=True)
app.include_router(auth.router)

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:8000",
    "https://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware)
app.add_middleware(ResponseLoggerMiddleware)

dotenv_path = os.path.join(os.path.dirname(__file__), "core", ".env")
load_dotenv(dotenv_path)


@app.get("/get")
async def start():
    return {"message": "hello world"}


@app.post("/store")
async def store_data(key: str, value: str):
    return {"message": "Data stored in Redis"}
