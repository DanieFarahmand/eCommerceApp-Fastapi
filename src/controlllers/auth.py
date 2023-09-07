from fastapi import HTTPException

from src.controlllers.user import UserController
from src.core.redis import RedisHandler
from src.core.exceptions import OTPError, UnauthorizedException
from src.utils.jwt import JWTHandler
from src.utils.otp import OTPHandler
from src.core.db.database import AsyncSession
from src.schemas.out.auth import Token


class AuthController:
    def __init__(self):
        self.redis_db = RedisHandler()
        self.otp_handler = OTPHandler()
        self.jwt_handler = JWTHandler()

    async def login(self, user_session_id: str, phone: str) -> None:
        try:
            otp_code = await self.otp_handler.send_otp_verify_code(phone=phone)
            registration_data = {
                "phone": phone,
                "otp_code": otp_code,
            }
            await self.redis_db.connect()
            await self.redis_db.set(name=user_session_id, value=registration_data, exp=90)
            await self.redis_db.disconnect()
        except OTPError as e:
            raise HTTPException(status_code=400, detail="Failed to send OTP code") from e

    async def verify_login(self, db_session: AsyncSession, otp_code, user_session_id: str) -> Token:
        try:
            await self.redis_db.connect()
            registration_data = await self.redis_db.get(name=user_session_id)

            if not registration_data:
                raise ValueError("Invalid Session_id")

            phone = registration_data["phone"]
            # Verify the OTP code provided by the user
            is_valid = await self.otp_handler.validate_otp_code(phone=phone, otp_code=otp_code)
            if is_valid:
                user = await UserController(db_session=db_session).get_user_by_phone(phone=phone)
                if not user:
                    user = await UserController(db_session=db_session).create_user(phone=phone)

                access_token = self.jwt_handler.encode_access_token(
                    payload={'user_id': str(user.id)})
                refresh_token = self.jwt_handler.encode_refresh_token(
                    payload={"sub": "refresh_token",
                             "verify": str(user.id)})
                csrf_token = self.jwt_handler.encode_refresh_token(
                    payload={
                        "sub": "csrf_token",
                        "refresh_token": str(refresh_token),
                        "access_token": str(access_token)
                    })
                # Store the refresh token in Redis
                await self.redis_db.set(name=refresh_token, value=user.id, exp=3600)
                await self.redis_db.disconnect()
                return Token(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    csrf_token=csrf_token,
                )
            else:
                raise HTTPException(status_code=401, detail="Invalid OTP code")
        except OTPError as e:
            raise HTTPException(status_code=400, detail="Failed to validate OTP code") from e

    async def logout(self, old_refresh_token: str) -> None:
        try:
            await self.redis_db.connect()
            user_id = await self.redis_db.get(name=old_refresh_token)
            if not user_id:
                raise UnauthorizedException(message="Invalid Refresh-Token")
            await self.redis_db.delete(name=old_refresh_token)
            await self.redis_db.disconnect()
        except UnauthorizedException as e:
            raise UnauthorizedException("Invalid Refresh-Token") from e

    async def refresh_token(self, old_refresh_token: str, session_id) -> Token:
        try:
            await self.redis_db.connect()
            user_id = await self.redis_db.get(name=old_refresh_token)
            if not user_id:
                raise UnauthorizedException("Invalid Refresh Token")
            stored_session_id = await self.redis_db.get(session_id)
            if stored_session_id != user_id:
                raise UnauthorizedException("Please verify using 2-step authentication first")
            access_token = self.jwt_handler.encode_access_token(payload={"user_id": str(user_id)})
            refresh_token = self.jwt_handler.encode_refresh_token(
                payload={"sub": "refresh_token", "verify": str(user_id)})
            csrf_token = self.jwt_handler.encode_refresh_token(
                payload={
                    "sub": "csrf_token",
                    "refresh_token": str(refresh_token),
                    "access_token": str(access_token)
                }
            )
            await self.redis_db.set(name=refresh_token, value=user_id, exp=3600)
            await self.redis_db.delete(name=old_refresh_token)
            await self.redis_db.disconnect()
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                csrf_token=csrf_token,
            )
        except UnauthorizedException as e:
            raise UnauthorizedException("Invalid Refresh Token") from e
