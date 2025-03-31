from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from ..adapters.token import AccessToken
from ..core.user import Session


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/yandex")


async def get_session(token_str: str = Depends(oauth2_scheme)) -> Session:
    try:
        token = AccessToken.from_jwt(token_str)
    except JWTError:
        raise CredentialsException()

    return await Session.get(id=token.claims["sid"])
