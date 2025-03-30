from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


from .utils import parse_user_agent
from ...config import DEBUG
from ...adapters import yandex
from ...adapters.token import AccessToken, RefreshToken
from ...db import OrmUser, RepositoryMixin
from . import repository
from .session import Session


class User(BaseModel, RepositoryMixin):
    id: UUID
    created_at: datetime
    email: str | None
    name: str | None
    surname: str | None
    is_admin: bool | None

    class Meta:
        orm_model = OrmUser
        
    @classmethod
    async def get(cls, **kwargs):
        user = await cls.db_get_or_none(**kwargs)
        if not user:
            raise HTTPException(404, "User not found.")
        return user

    @classmethod
    async def external_auth_login(cls, token: str, request: Request):
        external_user = await yandex.get_user_info(token)
        user_orm = await repository.get_user_by_external_id(external_user.id)
        if not user_orm:
            user_orm = await repository.create_user(
                external_user.email,
                external_user.first_name,
                external_user.last_name,
                external_user.id,
            )

        session_id = uuid4()
        claims = {"sub": str(user_orm.id), "sid": str(session_id)}
        access_token, refresh_token = AccessToken(claims), RefreshToken(claims)
        
        session = Session(
            id=session_id,
            user_id=user_orm.id,
            expires_at=refresh_token.expires,
            ip=request.client.host,
            user_agent=parse_user_agent(request.headers.get("user-agent")),
            is_deactivated=False,
        )
        await session.db_create()
        
        response = JSONResponse({"access_token": access_token.to_jwt()}, status_code=201)
        response.set_cookie(
            key="session_token",
            value=refresh_token.to_jwt(),
            max_age=refresh_token.exp,
            samesite='strict',
            httponly=True,
            secure=True if not DEBUG else False,
        )
        return response
    
    @classmethod
    async def logout(cls, session_id):
        session = await Session.db_get_or_none(id=session_id)
        if not session or not session.is_valid:
            raise HTTPException(404, "Session not found.")
        await session.db_update_fields(is_deactivated=True)

    @classmethod
    async def update(cls, user_id, **kwargs):
        user = await cls.get(id=user_id)
        await user.db_update_fields(**kwargs)
        
    @classmethod
    async def delete(cls, user_id):
        user = await cls.get(id=user_id)
        await user.db_delete()
        await repository.deactivate_all_sessions(user_id)
