from passlib.context import CryptContext


class PasswordHandler:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )

    @classmethod
    def hash(cls, password: str):
        return PasswordHandler.pwd_context.hash(password)

    @classmethod
    def verify(cls, password: str, hashed_password: str):
        return cls.pwd_context.verify(password, hashed_password)
