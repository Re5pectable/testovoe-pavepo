from fastapi import APIRouter, Body, Request, Depends
from ...core.user import User, Session
from ..auth import get_session

router = APIRouter()


@router.post("/login/yandex")
async def yandex_login(request: Request, token: str = Body(embed=True)):
    return await User.external_auth_login(token, request)


@router.post("/logout")
async def logout(request: Request, session: Session = Depends(get_session)):
    await session.deactivate()

