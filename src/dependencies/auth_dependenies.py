from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.db.database import AsyncSession, get_session
from src.core.exceptions import ForbiddenException
from src.models.user import User
from src.utils.jwt import JWTHandler

http_bearer = HTTPBearer()


async def get_current_user(
        request: Request, credential: HTTPAuthorizationCredentials = Depends(http_bearer)):
    if credential.scheme != "Bearer":
        raise ForbiddenException("Invalid Header")
    access_token = request.cookies.get("Access-Token")
    if not access_token:
        raise ForbiddenException('Access-Token is not provided')
    token = JWTHandler.decode_token(access_token)
    user_id = token.get("user_id")
    if not user_id:
        raise ForbiddenException("Invalid Access Token")

    csrf_token = JWTHandler.decode_token(credential.credentials)
    if csrf_token.get("access_token") != access_token:
        raise ForbiddenException("Invalid CSRF Token")
    return user_id


async def get_current_user_with_refresh(
        request: Request, credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    if credentials.scheme != "Bearer":
        raise ForbiddenException("Invalid Header")
    refresh_token = request.cookies.get("Refresh-Token")
    if not refresh_token:
        raise ForbiddenException("Refresh-Token is not provided")
    token = JWTHandler.decode_token(refresh_token)
    user_id = token.get("verify")
    if not user_id:
        raise ForbiddenException("Invalid Refresh Token")
    csrf_token = JWTHandler.decode_token(credentials.credentials)
    if csrf_token.get("refresh_token") != refresh_token:
        raise ForbiddenException("Invalid CSRF Token")
    return user_id


async def get_current_user_from_db(
        db_session: AsyncSession = Depends(get_session), user_id: str = Depends(get_current_user)):
    user = await db_session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found in the database")
    return user
