from fastapi import APIRouter, Body, Depends, Request, Cookie, HTTPException
from jose import JWTError

from ...core.user import Session, User
from ..auth import get_session
from ..handler import api_handler
from ...adapters.token import RefreshToken
from ..schemas import AccessToken

router = APIRouter()


@router.post("/login/yandex")
@api_handler()
async def yandex_login(request: Request, token: str | None = Body(None, embed=True)):
    return await User.external_auth_login(token, request)


@router.post("/logout")
@api_handler()
async def logout(request: Request, session: Session = Depends(get_session)):
    await session.deactivate()


@router.post("/new-access-token", response_model=AccessToken)
@api_handler()
async def new_access_token(request: Request, refresh_token: str = Cookie(None)):
    try:
        token = RefreshToken.from_jwt(refresh_token)
    except JWTError:
        raise HTTPException(401)
    session = await Session.get(id=token.claims["sid"])
    return session.get_access_token()
