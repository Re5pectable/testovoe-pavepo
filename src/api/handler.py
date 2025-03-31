import json
import logging
import traceback as tb
from functools import wraps
from typing import Callable

from fastapi import HTTPException, Response
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..config import DEBUG
from ..core.user import Session, User
from ..db import OrmApiLog, UnitOfWork


async def _get_body(request: Request):
    try:
        body = await request.body()
        body = json.loads(body.decode())    
    except Exception:
        return None
    if request.url.path == "/login/yandex":
        body["token"] = "***"
    return body

async def _validate_admin(session: Session | None):
    if not session:
        raise HTTPException(401)
    user = await User.get(id=session.user_id)
    if not user:
        raise HTTPException(401)
    if not user.is_admin:
        raise HTTPException(403)


def api_handler(admin: bool = False):
    def decorator(f: Callable):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            session: Session = kwargs.get("session")

            headers = dict(request.headers)
            cookies = dict(request.cookies)
            query = dict(request.query_params)
            body = await _get_body(request)
            method = request.method
            uri = request.url.path

            status_code = 200
            tb_str = None
            try:
                if admin:
                   await _validate_admin(session)
                
                response = await f(*args, **kwargs)
                
                if isinstance(response, Response):
                    status_code = response.status_code
                
                return response
            
            except HTTPException as e:
                status_code = e.status_code
                raise e
                
            except Exception:
                tb_str = tb.format_exc()
                if DEBUG:
                    logging.debug(tb_str)
                status_code = 400
                response = JSONResponse(
                    {"detail": "Unexpected error"}, status_code=status_code
                )
                return response
            finally:
                async with UnitOfWork() as db_session:
                    log = OrmApiLog(
                        uri=uri,
                        method=method,
                        headers=headers,
                        cookies=cookies,
                        session_id=session.id if session else None,
                        query=query,
                        body=body,
                        status_code=status_code,
                        traceback=tb_str,
                    )
                    db_session.add(log)

        return wrapper

    return decorator
