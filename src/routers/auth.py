from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response, HTTPException

from src.controlllers.auth import AuthController
from src.core.db.database import AsyncSession, get_session
from src.core.exceptions import UserAlreadyExistsException, UnauthorizedException
from src.core.redis import RedisHandler
from src.schemas._in.auth import RegistrationIn, OTPCodeIn, LoginByEmailIn, LoginByPhoneIn
from src.dependencies.auth_dependenies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])
redis_handler = RedisHandler()


@router.post("/register/")
async def register(request: Request, user_data: RegistrationIn):
    try:
        user_session_id = request.cookies.get("Session_Id", "")
        return await AuthController().register_user(
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone,
            user_session_id=user_session_id,
        )
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post("/verify/")
async def verify_registration(
        request: Request, response: Response, otp_code: OTPCodeIn,
        db_session: AsyncSession = Depends(get_session)):
    user_session_id = request.cookies.get("Session_Id", "")
    try:
        tokens = await AuthController().verify_registration(
            db_session=db_session,
            user_session_id=user_session_id,
            otp_code=otp_code.code,
        )
        response.set_cookie(
            key="Refresh_Token",
            value=tokens.refresh_token,
            secure=True,
            httponly=True,
            samesite="strict",
        )
        response.set_cookie(
            key="Access-Token",
            value=tokens.access_token,
            secure=True,
            httponly=True,
            samesite="strict",
        )

        response.headers["X-CSRF-TOKEN"] = tokens.csrf_token
        return {"message": "Verification successful", "tokens": tokens}  # tokens are passed just for test.
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post("/login/")
async def login_by_email(user_data: LoginByEmailIn, response: Response,
                         db_session: AsyncSession = Depends(get_session)):
    tokens = await AuthController().login_by_email(
        session=db_session, email=user_data.email,
        password=user_data.password,
    )
    try:
        response.set_cookie(
            key="Access-Token",
            value=tokens.access_token,
            secure=True,
            httponly=True,
            samesite="strict",
        )
        response.set_cookie(
            key="Refresh_Token",
            value=tokens.refresh_token,
            secure=True,
            httponly=True,
            samesite="strict",
        )

        response.headers["X-CSRF-TOKEN"] = tokens.csrf_token
        return {"message": "Login was successful", "tokens": tokens}  # tokens are passed just for test.
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post("/login-by-phone/")
async def login_by_phone(request: Request, user_data: LoginByPhoneIn, db_session: AsyncSession = Depends(get_session)):
    try:
        user_session_id = request.cookies.get("Session_Id", "")
        return await AuthController().login_by_phone(
            user_session_id=user_session_id,
            session=db_session,
            phone=user_data.phone
        )
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post("/login-by-phone/verify/")
async def verify_login_by_phone(request: Request, code: str, response: Response):
    user_session_id = request.cookies.get("Session_Id", "")
    try:
        tokens = await AuthController().verify_login_by_phone(
            user_session_id=user_session_id, otp_code=code)
        response.set_cookie(
            key="Refresh_Token",
            value=tokens.refresh_token,
            secure=True,
            httponly=True,
            samesite="strict",
        )
        response.set_cookie(
            key="Access-Token",
            value=tokens.access_token,
            secure=True,
            httponly=True,
            samesite="strict",

        )

        response.headers["X-CSRF-TOKEN"] = tokens.csrf_token
        return {"message": "Login was successful", "tokens": tokens}  # tokens are passed just for test.
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))


@router.post("/logout/")
async def logout(request: Request, response: Response, current_user: str = Depends(get_current_user)):
    old_refresh_token = request.cookies.get("Refresh_Token", "")
    try:
        await AuthController().logout(old_refresh_token=old_refresh_token)
        response.set_cookie(
            key="Refresh_Token",
            value="",
            secure=True,
            httponly=True,
            samesite="strict",
            max_age=0,
        )
        response.set_cookie(
            key="Access-Token",
            value="",
            secure=True,
            httponly=True,
            samesite="strict",
            max_age=0,
        )
        return {"message": "Logout was successful"}
    except UnauthorizedException as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))


@router.post("/refresh/")
async def refresh_token(
        response: Response,
        request: Request,
        user_id: str = Depends(get_current_user),
        db_session: AsyncSession = Depends(get_session)):
    try:
        tokens = await AuthController().refresh_token(
            old_refresh_token=request.cookies.get("Refresh-Token", ""),
            session_id=request.cookies.get("Session_Id", "")
        )
        if tokens:
            response.set_cookie(
                key="Refresh-Token",
                value=tokens.refresh_token,
                secure=True,
                httponly=True,
                samesite="strict",
            )
            response.set_cookie(
                key="Access-Token",
                value=tokens.access_token,
                secure=True,
                httponly=True,
                samesite="strict",
            )
    except UnauthorizedException as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))
