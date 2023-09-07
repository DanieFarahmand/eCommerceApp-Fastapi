from secrets import token_hex

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.core.config import settings


class SessionMiddleware(BaseHTTPMiddleware):

    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
            app_settings=settings,
    ) -> Response:
        session_id = request.cookies.get("Session_Id")
        if not session_id:
            session_id = token_hex(16)
        response = await call_next(request)
        response.set_cookie(
            "Session_Id",
            session_id,
            max_age=app_settings.SESSION_EXPIRE_MINUTES,
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )
        return response
