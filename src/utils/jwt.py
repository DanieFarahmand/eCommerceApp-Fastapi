from typing import Dict, Any
from datetime import datetime, timedelta

from jose import jwt, ExpiredSignatureError, JWTError
from fastapi.security import HTTPBearer

from src.core.exceptions import CustomException
from src.core.config import settings


class JWTExpiredTokenException(CustomException):
    status_code = 401
    message = "Expired token"


class JWTInvalidTokenException(CustomException):
    status_code = 401
    message = "Invalid token"


class JWTHandler(HTTPBearer):
    access_token_expire = settings.ACCESS_TOKEN_EXPIRE
    refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE
    secret_key = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM

    @staticmethod
    def encode_access_token(payload: Dict[str, Any]) -> str:
        expire = datetime.utcnow() + timedelta(minutes=JWTHandler.access_token_expire)
        payload.update({"exp": expire})
        return jwt.encode(payload, JWTHandler.secret_key, JWTHandler.algorithm)

    @staticmethod
    def encode_refresh_token(payload: Dict[str, Any]) -> str:
        expire = datetime.utcnow() + timedelta(minutes=JWTHandler.refresh_token_expire)
        payload.update({"exp": expire})
        return jwt.encode(payload, JWTHandler.secret_key, JWTHandler.algorithm)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm])
        except ExpiredSignatureError as exception:
            raise JWTExpiredTokenException() from exception
        except JWTError as exception:
            raise JWTInvalidTokenException() from exception

    @staticmethod
    def decode_refresh_token(token: str) -> dict:
        try:
            return jwt.decode(
                token, JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False})
        except JWTError as exception:
            raise JWTExpiredTokenException() from exception

