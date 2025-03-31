from uuid import UUID

from fastapi import APIRouter, Body, Depends, Request

from ...core.user import Session, User
from ..auth import get_session
from ..handler import api_handler

router = APIRouter()


@router.delete("/user")
@api_handler(admin=True)
async def delete_user(
    request: Request,
    user_id: UUID = Body(embed=True),
    session: Session = Depends(get_session),
):
    await User.delete(user_id)
