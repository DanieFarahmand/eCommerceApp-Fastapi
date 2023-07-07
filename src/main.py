import os

from dotenv import load_dotenv
from fastapi import FastAPI
from src.routers import user

dotenv_path = os.path.join(os.path.dirname(__file__), "core", ".env")
load_dotenv(dotenv_path)

app = FastAPI(debug=True)
app.include_router(user.router)


@app.get("/")
async def startup():
    return {"message": "hello world"}
