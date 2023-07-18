from fastapi import APIRouter, Depends, Response, HTTPException

from src.controlllers.auth import AuthController
from src.core.db.database import AsyncSession, get_session
from src.core.redis import RedisHandler
from src.models.user import User
from src.schemas._in.auth import RegistrationIn

router = APIRouter(tags=["Auth"])
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


@router.delete("/delete")
async def delete_user(user_id: int, db_session: AsyncSession = Depends(get_session)):
    await User().delete_user(session=db_session, user_id=user_id)
    return {"message": "User deleted"}

# {
#   "phone": "09173642416",
#   "email": "danie.0098.sh@gmail.com",
#   "password": "Danie0098"
# }
