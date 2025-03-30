import traceback as tb

from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from ..adapters.token import Token
from ..db import OrmApiLog, UnitOfWork


def _extract_session_id(headers: dict[str, str]):
    auth = headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    
    token_str = auth.removeprefix("Bearer ")
    try:
        token = Token.from_jwt(token_str)
        return token.claims.get("sid")
    except JWTError:
        return None

async def _get_body(request: Request):
    body = await request.json()
    if request.url == "/login/yandex":
        print(123)
    return body
    

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        headers = dict(request.headers)
        cookies = dict(request.cookies)
        query = dict(request.query_params)
        body = await _get_body(request)
        method = request.method
        uri = str(request.url)
        session_id = _extract_session_id(request.headers)

        status_code = 200
        tb_str = None
        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            tb_str = tb.format_exc()
            status_code = 400
            response = JSONResponse({"detail": "Unexpected error"}, status_code=400)

        async with UnitOfWork() as session:
            log = OrmApiLog(
                uri=uri,
                method=method,
                headers=headers,
                cookies=cookies,
                session_id=session_id,
                query=query,
                body=body,
                status_code=status_code,
                traceback=tb_str,
            )
            session.add(log)

        return response