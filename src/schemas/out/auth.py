from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str


class Token(BaseModel):
    refresh_token: str | None
    access_token: str
    csrf_token: str
