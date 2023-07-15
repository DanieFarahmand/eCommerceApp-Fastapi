import asyncio
from datetime import datetime, timedelta
import random
from sms_ir import SmsIr
from src.core.config import settings
from src.core.redis import RedisHandler

api_key = settings.SMS_API_KEY
otp_code_length = settings.OTP_CODE_LENGTH


class OTPHandler:
    def __init__(self):
        self.sms_ir = SmsIr(api_key=api_key)
        self.redis_db = RedisHandler()

    @staticmethod
    async def generate_code():
        digits = "0123456789"
        otp_code = "".join(random.choice(digits) for _ in range(otp_code_length))
        return otp_code

    async def send_otp_verify_code(self, phone):
        template_id = 100000
        try:
            otp = await self.generate_code()
            parameters = {"name": "code", "value": otp}
            self.sms_ir.send_verify_code(
                number=phone, parameters=[parameters], template_id=template_id)

            expiration_time = datetime.now() + timedelta(seconds=300)  # Calculate expiration time
            expiration_time_str = expiration_time.strftime('%Y-%m-%d %H:%M:%S')  # Serialize expiration time to string

            await self.redis_db.connect()
            await self.redis_db.set(name=phone, value={"otp": otp, "exp": expiration_time_str}, exp=300)
            return otp
        except Exception as e:
            raise ValueError("Failed to send OTP code") from e
        finally:
            await self.redis_db.disconnect()

    async def validate_otp_code(self, phone, otp_code):
        try:
            await self.redis_db.connect()
            stored_otp_data = await self.redis_db.get(name=phone)

            if stored_otp_data and "otp" in stored_otp_data and "exp" in stored_otp_data:
                stored_otp_code = stored_otp_data["otp"]
                expiration_time_str = stored_otp_data["exp"]
                expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M:%S")
                current_time = datetime.now()

                if current_time <= expiration_time and otp_code == stored_otp_code:
                    await self.redis_db.delete(name=phone)
                    return True
                else:
                    return False  # Invalid OTP code or expired
            else:
                return False  # OTP data not found or incomplete
        except Exception as e:
            raise ValueError("Failed to validate OTP code") from e
        finally:
            await self.redis_db.disconnect()
