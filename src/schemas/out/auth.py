from typing import Optional

from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str


class Token(BaseModel):
    refresh_token: Optional[str]
    access_token: Optional[str]
    csrf_token: str
