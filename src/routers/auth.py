from http import HTTPStatus
import logging

from fastapi import APIRouter, Depends, Request, Response, HTTPException

from src.controlllers.auth import AuthController
from src.core.db.database import AsyncSession, get_session
from src.core.exceptions import UserAlreadyExistsException, UnauthorizedException
from src.core.redis import RedisHandler, get_redis
from src.schemas._in.auth import LoginDataIn, OTPCodeIn
from src.dependencies.auth_dependenies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])
redis_handler = RedisHandler()
logger = logging.getLogger(__name__)


@router.post("/login/")
async def login(request: Request, user_data: LoginDataIn, redis_db: RedisHandler = Depends(get_redis)):
    try:
        user_session_id = request.cookies.get("Session_Id", "")
        await AuthController(redis_db=redis_db).login(
            phone=user_data.phone,
            user_session_id=user_session_id,
        )
        return {"message": "OTP code sent."}
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post("/verify/")
async def verify_login(
        request: Request, response: Response, otp_code: OTPCodeIn,
        redis_db: RedisHandler = Depends(get_redis),
        db_session: AsyncSession = Depends(get_session)):
    user_session_id = request.cookies.get("Session_Id", "")
    try:
        tokens = await AuthController(redis_db=redis_db).verify_login(
            db_session=db_session,
            user_session_id=user_session_id,
            otp_code=otp_code.code,
        )
        response.set_cookie(
            key="Refresh-Token",
            value=tokens.refresh_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/"

        )
        response.set_cookie(
            key="Access-Token",
            value=tokens.access_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )

        response.headers["X-CSRF-TOKEN"] = tokens.csrf_token

        return {"message": "Verification successful"}
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post("/logout/")
async def logout(
        response: Response,
        request: Request,
        redis_db: RedisHandler = Depends(get_redis),
        current_user: str = Depends(get_current_user)):
    old_refresh_token = request.cookies.get("Refresh-Token", "")

    try:
        await AuthController(redis_db=redis_db).logout(old_refresh_token=old_refresh_token)
        response.set_cookie(
            key="Refresh-Token",
            value="",
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )
        response.set_cookie(
            key="Access-Token",
            value="",
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )

        return {"message": "Logout was successful"}
    except UnauthorizedException as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))


@router.post("/refresh/")
async def refresh_token(
        response: Response,
        request: Request,
        user_id: str = Depends(get_current_user),
        redis_db: RedisHandler = Depends(get_redis),
        db_session: AsyncSession = Depends(get_session)):
    try:
        tokens = await AuthController(redis_db=redis_db).refresh_token(
            old_refresh_token=request.cookies.get("Refresh-Token", ""),
            session_id=request.cookies.get("Session_Id", "")
        )
        if tokens:
            response.set_cookie(
                key="Refresh-Token",
                value=tokens.refresh_token,
                httponly=True,
                secure=True,
                samesite="none",
                path="/"

            )
            response.set_cookie(
                key="Access-Token",
                value=tokens.access_token,
                httponly=True,
                secure=True,
                samesite="none",
                path="/"
            )
            response.headers["X-CSRF-TOKEN"] = tokens.csrf_token
            return {"message": "Token refreshed."}
    except UnauthorizedException as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))
