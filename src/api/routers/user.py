from fastapi import APIRouter, Request, Depends
from ..auth import get_session
from ...core.user import User, Session
from ..payloads import UserUpdate

router = APIRouter()


@router.get("")
async def get_me(request: Request, session: Session = Depends(get_session)):
    return await User.get(id=session.user_id)


@router.put("")
async def update_me(
    data: UserUpdate, session: Session = Depends(get_session)
):
    await User.update(session.user_id, **data.model_dump())
