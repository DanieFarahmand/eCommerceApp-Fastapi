from datetime import datetime
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
        otp_code = ""
        for i in range(otp_code_length):
            otp_code += random.choice(digits)
        return otp_code

    async def send_otp_verify_code(self, phone):
        template_id = 10000
        otp = self.generate_code()
        parameters = {"name": "code", "value": otp}
        self.sms_ir.send_verify_code(
            number=phone, parameters=[parameters], template_id=template_id)
        await self.redis_db.set(name=phone, value=otp, exp=300)

    async def validate_otp_code(self, phone, otp_code):
        otp_data = await self.redis_db.get(phone)
        if otp_data and "exp" in otp_data:
            expiration_time_str = otp_data["exp"]
            expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            if current_time <= expiration_time and otp_code == otp_data["otp"]:
                await self.redis_db.delete(phone)
                return True
        return False
