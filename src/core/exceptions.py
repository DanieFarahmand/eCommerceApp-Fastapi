from http import HTTPStatus


class CustomException(Exception):
    status_code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


class UserAlreadyExistsException(CustomException):
    status_code = HTTPStatus.CONFLICT
    error_code = "user_already_exists"
    message = HTTPStatus.CONFLICT.description

    def __init__(self, message=None):
        if message:
            self.message = message


class ForbiddenException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description

    def __init__(self, message=None):
        if message:
            self.message = message
