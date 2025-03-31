from fastapi import APIRouter, Depends, Request

from ...core.user import Session, User
from ..auth import get_session
from ..handler import api_handler
from ..schemas import UserUpdate

router = APIRouter()


@router.get("", response_model=User)
@api_handler()
async def get_me(request: Request, session: Session = Depends(get_session)):
    return await User.get(id=session.user_id)


@router.put("")
@api_handler()
async def update_me(
    request: Request, data: UserUpdate, session: Session = Depends(get_session)
):
    await User.update(session.user_id, **data.model_dump(exclude_none=True))
