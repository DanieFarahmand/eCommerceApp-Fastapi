from fastapi import APIRouter, Depends, Request, Response, HTTPException

from src.controlllers.auth import AuthController
from src.core.db.database import AsyncSession, get_session
from src.core.redis import RedisHandler
from src.models.user import User
from src.schemas._in.auth import RegistrationIn, LoginByEmailIn, LoginByPhoneIn
from src.dependencies.auth_dependenies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])
redis_handler = RedisHandler()


@router.post("/register/")
async def register(user_data: RegistrationIn):
    return await AuthController().register_user(
        email=user_data.email,
        password=user_data.password,
        phone=user_data.phone,
    )


@router.post("/verify/{unique_identifier}/")
async def verify_registration(
        unique_identifier: str, response: Response, otp_code: str,
        db_session: AsyncSession = Depends(get_session)):
    try:
        tokens = await AuthController().verify_registration(
            db_session=db_session,
            unique_identifier=unique_identifier,
            otp_code=otp_code,
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
        return {"message": "Verification successful"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login/")
async def login_by_email(user_data: LoginByEmailIn, response: Response,
                         db_session: AsyncSession = Depends(get_session)):
    tokens = await AuthController().login_by_email(
        session=db_session, email=user_data.email,
        password=user_data.password,
    )
    try:
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
        return {"message": "Login was successful"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login-by-phone/")
async def login_by_phone(user_data: LoginByPhoneIn, db_session: AsyncSession = Depends(get_session)):
    return await AuthController().login_by_phone(session=db_session, phone=user_data.phone)


@router.post("/login-by-phone/verify/")
async def veridy_login_by_phone(unique_id: str, code: str, response: Response):
    try:
        tokens = await AuthController().verify_login_by_phone(unique_id=unique_id, otp_code=code)
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
        return {"message": "Login was successful"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/logout/")
async def logout(request: Request, response: Response, current_user: str = Depends(get_current_user)):
    await AuthController().logout(old_refresh_token=request.cookies.get("Refresh-Token", ""))
    response.set_cookie(
        key="Refresh-Token",
        value="",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.set_cookie(
        key="Access-Token",
        value="",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return {"message": "Logout was successful"}


@router.delete("/delete")
async def delete_user(user_id: int, db_session: AsyncSession = Depends(get_session)):
    await User().delete_user(session=db_session, user_id=user_id)
    return {"message": "User deleted"}

