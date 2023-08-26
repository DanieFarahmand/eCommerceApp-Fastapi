import re

from pydantic import BaseModel, EmailStr, EmailError, Field, validator


class RegistrationIn(BaseModel):
    phone: str
    email: str
    password: str = Field(min_length=8)

    @validator("phone")
    def validate_phone(cls, phone):
        regex = r"((0?9)|(\+?989))((14)|(13)|(12)|(19)|(18)|(17)|(15)|(16)|(11)|(10)|(90)|(91)|(92)|(93)|(94)|(95)|(96)|(32)|(30)|(33)|(35)|(36)|(37)|(38)|(39)|(00)|(01)|(02)|(03)|(04)|(05)|(41)|(20)|(21)|(22)|(23)|(31)|(34)|(9910)|(9911)|(9913)|(9914)|(9999)|(999)|(990)|(9810)|(9811)|(9812)|(9813)|(9814)|(9815)|(9816)|(9817)|(998))\W?\d{3}\W?\d{4}"
        matches = re.finditer(regex, phone)
        if matches:
            return phone

    @validator("email")
    def validate_email(cls, email: str):
        if not email.endswith("@gmail.com"):
            raise EmailError()
        return email


class LoginByEmailIn(BaseModel):
    email: str
    password: str = Field(min_length=8)

    @validator("email")
    def validate_email(cls, email: str):
        if not email.endswith("@gmail.com"):
            raise EmailError()
        return email


class LoginByPhoneIn(BaseModel):
    phone: str

    @validator("phone")
    def validate_phone(cls, phone):
        regex = r"((0?9)|(\+?989))((14)|(13)|(12)|(19)|(18)|(17)|(15)|(16)|(11)|(10)|(90)|(91)|(92)|(93)|(94)|(95)|(96)|(32)|(30)|(33)|(35)|(36)|(37)|(38)|(39)|(00)|(01)|(02)|(03)|(04)|(05)|(41)|(20)|(21)|(22)|(23)|(31)|(34)|(9910)|(9911)|(9913)|(9914)|(9999)|(999)|(990)|(9810)|(9811)|(9812)|(9813)|(9814)|(9815)|(9816)|(9817)|(998))\W?\d{3}\W?\d{4}"
        matches = re.finditer(regex, phone)
        if matches:
            return phone


class OTPCodeIn(BaseModel):
    code: str
