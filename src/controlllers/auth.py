from fastapi import HTTPException

from src.models.user import User
from src.core.db.database import AsyncSession
from src.utils.jwt import JWTHandler
from src.utils.otp import OTPHandler


class OTPAuth:
    @staticmethod
    async def register(phone):
        otp_code = await OTPHandler().send_otp_verify_code(phone=phone)
        return otp_code

    @staticmethod
    async def verify(session: AsyncSession, phone, otp_code):
        is_valid = await OTPHandler().validate_otp_code(phone=phone, otp_code=otp_code)
        if is_valid:
            new_user = await User().create_user_by_phone(session=session, phone=phone)
            payload = {"user_id": new_user.id}
            token = JWTHandler().generate_tokens(payload=payload)
            return token
        else:
            raise HTTPException(status_code=401, detail="Invalid OTP code")

    async def login(self, *args, **kwargs):
        ...

    async def logout(self, *args, **kwargs):
        ...

    async def password_reset(self, *args, **kwargs):
        ...
