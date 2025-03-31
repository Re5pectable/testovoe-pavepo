from fastapi import APIRouter, Depends, File, Request, UploadFile

from ...core.media import Media
from ...core.user import Session
from ..auth import get_session
from ..handler import api_handler

router = APIRouter()


@router.get("", response_model=list[Media])
@api_handler()
async def get_all(request: Request, session: Session = Depends(get_session)):
    return await Media.db_get_many(user_id=session.user_id)


@router.post("")
@api_handler()
async def upload(
    request: Request,
    file: UploadFile = File(None),
    session: Session = Depends(get_session),
):
    await Media.create(session.user_id, file)
