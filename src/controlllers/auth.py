import uuid

from fastapi import HTTPException

from src.models.user import User
from src.core.redis import RedisHandler
from src.core.exceptions import OTPError, UnauthorizedException
from src.utils.jwt import JWTHandler
from src.utils.password import PasswordHandler
from src.utils.otp import OTPHandler
from src.core.db.database import AsyncSession
from src.schemas.out.auth import Token


class AuthController:
    def __init__(self):
        self.redis_db = RedisHandler()
        self.otp_handler = OTPHandler()
        self.jwt_handler = JWTHandler()

    async def register_user(self, email: str, password: str, phone: str):
        try:
            otp_code = await self.otp_handler.send_otp_verify_code(phone=phone)
            registration_data = {
                "email": email,
                "phone": phone,
                "password": password,
                "otp_code": otp_code,
            }
            unique_identifier = str(uuid.uuid4())
            await self.redis_db.connect()
            await self.redis_db.set(name=unique_identifier, value=registration_data, exp=90)
            await self.redis_db.disconnect()
            return {"unique_identifier": unique_identifier}
        except OTPError as e:
            raise HTTPException(status_code=400, detail="Failed to send OTP code") from e

    async def verify_registration(self, db_session: AsyncSession, otp_code: str, unique_identifier: str) -> Token:
        try:
            await self.redis_db.connect()
            registration_data = await self.redis_db.get(name=unique_identifier)

            if not registration_data:
                ...
            email = registration_data["email"]
            password = registration_data["password"]
            phone = registration_data["phone"]

            # Verify the OTP code provided by the user
            is_valid = await self.otp_handler.validate_otp_code(phone=phone, otp_code=otp_code)
            if is_valid:
                new_user = await User.create_user(session=db_session, email=email, password=password, phone=phone)
                access_token = self.jwt_handler.encode_access_token(payload={'user_id': str(new_user.id)})
                refresh_token = self.jwt_handler.encode_refresh_token(
                    payload={"sub": "refresh_token", "verify": str(new_user.id)}
                )
                csrf_token = self.jwt_handler.encode_refresh_token(
                    payload={
                        "sub": "csrf_token",
                        "refresh_token": str(refresh_token),
                        "access_token": str(access_token),
                    }
                )
                # Store the refresh token in Redis
                await self.redis_db.set(name=refresh_token, value=new_user.id, exp=3600)
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
            raise HTTPException(status_code=401, detail=str(e)) from e

    async def login_by_email(self, session: AsyncSession, email: str, password: str) -> Token:
        user = await User.get_user_by_email(session=session, email=email)
        if not user:
            raise ValueError("User with this email does not exist")
        if PasswordHandler().verify(password=password, hashed_password=user.password):
            access_token = self.jwt_handler.encode_access_token(payload={"user_id": str(user.id)})
            refresh_token = self.jwt_handler.encode_refresh_token(
                payload={"sub": "refresh_token", "verify": str(user.id)})
            csrf_token = self.jwt_handler.encode_refresh_token(
                payload={
                    "sub": "csrf_token",
                    "refresh_token": str(refresh_token),
                    "access_token": str(access_token),
                }
            )
            await self.redis_db.set(name=refresh_token, value=user.id, exp=3600)
            await self.redis_db.disconnect()
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                csrf_token=csrf_token,
            )
        else:
            raise ValueError("Password is not correct")

    async def login_by_phone(self, session: AsyncSession, phone: str):
        user = await User.get_user_by_phone(session=session, phone=phone)
        if not user:
            raise ValueError("User with this phone number does not exist.")
        otp_code = await self.otp_handler.send_otp_verify_code(phone=phone)
        login_data = {"phone": phone, "user": user.id, "otp_code": otp_code}
        unique_identifier = str(uuid.uuid4())
        await self.redis_db.connect()
        await self.redis_db.set(name=unique_identifier, value=login_data, exp=90)
        await self.redis_db.disconnect()
        return unique_identifier

    async def verify_login_by_phone(self , unique_id: str, otp_code: str):
        await self.redis_db.connect()
        login_data = await self.redis_db.get(name=unique_id)
        is_valid = await self.otp_handler.validate_otp_code(phone=login_data["phone"], otp_code=otp_code)
        if is_valid:
            access_token = self.jwt_handler.encode_access_token(payload={"user_id": str(login_data["user"])})
            refresh_token = self.jwt_handler.encode_refresh_token(
                payload={"sub": "refresh_token", "verify": str(login_data["user"])})
            csrf_token = self.jwt_handler.encode_refresh_token(
                payload={
                    "sub": "csrf_token",
                    "refresh_token": str(refresh_token),
                    "access_token": str(access_token),
                }
            )
            await self.redis_db.set(name=refresh_token, value=login_data["user"], exp=3600)
            await self.redis_db.disconnect()
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                csrf_token=csrf_token,
            )
        else:
            raise OTPError(message="Invalid OTP code.")

    async def logout(self, old_refresh_token: str) -> None:
        try:
            await self.redis_db.connect()
            user_id = await self.redis_db.get(name=old_refresh_token)
            if not user_id:
                raise UnauthorizedException(message="Invalid Refresh-Token")
            await self.redis_db.delete(name=old_refresh_token)
            await self.redis_db.disconnect()
        except UnauthorizedException as e:
            raise HTTPException(status_code=401, detail=str(e))

    async def get_user_info(self, user_id: str) -> User:
        ...
