import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth, user, product, category
from src.core.middlewares.session import SessionMiddleware
from src.core.middlewares.response_logger import ResponseLoggerMiddleware

app = FastAPI(debug=True)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(category.router)

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:8000",
    "https://localhost:8000",
    "http://127.0.0.1:5174",
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
