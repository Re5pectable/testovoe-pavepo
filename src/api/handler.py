import traceback as tb
import json
from typing import Callable
from functools import wraps

from jose import JWTError
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

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
    body = await request.body()
    body = body.decode()
    if not body:
        return None
    body = json.loads(body)
    if request.url.path == "/login/yandex":
        body["token"] = "***"
    return body


def api_handler(admin: bool = False):
    def decorator(f: Callable):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")

            headers = dict(request.headers)
            cookies = dict(request.cookies)
            query = dict(request.query_params)
            body = await _get_body(request)
            method = request.method
            uri = request.url.path
            session_id = _extract_session_id(request.headers)

            status_code = 200
            tb_str = None
            try:
                response = await f(*args, **kwargs)
                status_code = response.status_code
                return response
            
            except HTTPException as e:
                status_code = e.status_code
                raise e
                
            except Exception:
                tb_str = tb.format_exc()
                status_code = 400
                response = JSONResponse(
                    {"detail": "Unexpected error"}, status_code=status_code
                )
            finally:
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

        return wrapper

    return decorator
