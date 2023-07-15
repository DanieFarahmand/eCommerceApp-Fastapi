from fastapi import APIRouter, Depends, Response, HTTPException

from src.controlllers.auth import OTPAuth
from src.core.db.database import AsyncSession, get_session
from src.core.redis import RedisHandler

router = APIRouter(tags=["Auth"])
redis_handler = RedisHandler()


@router.post("/register/")
async def register(phone: str, response: Response):
    otp_code = await  OTPAuth.register(phone=phone)
    response.headers["Location"] = f"/verify/{phone}"
    return {"otp_code": otp_code, "phone": phone}


@router.post("/verify/{phone}/")
async def verify(phone: str, code: str, db_session: AsyncSession = Depends(get_session)):
    try:
        user_token = await OTPAuth.verify(session=db_session, phone=phone, otp_code=code)
        return {"user_token": user_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
