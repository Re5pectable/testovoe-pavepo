from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..adapters.token import AccessToken
from ..core.user import Session


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/")


async def get_session(token_str: str = Depends(oauth2_scheme)):
    token = AccessToken.from_jwt(token_str)

    session = await Session.db_get_or_none(id=token.claims["sid"])
    if not session or not session.is_valid:
        raise CredentialsException()

    return session
