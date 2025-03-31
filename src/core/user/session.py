from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from ...db import OrmSession, RepositoryMixin
from ...adapters.token import AccessToken


class Session(BaseModel, RepositoryMixin):

    id: UUID
    user_id: UUID
    expires_at: datetime
    ip: str
    user_agent: dict
    is_deactivated: bool
    
    model_config = ConfigDict(from_attributes=True)

    class Meta:
        orm_model = OrmSession

    @property
    def is_valid(self):
        if self.is_deactivated:
            return False
        if self.expires_at < datetime.now():
            return False
        return True
    
    @classmethod
    async def get(cls, **kwargs):
        session = await cls.db_get_or_none(**kwargs)
        if not session or not session.is_valid:
            raise HTTPException(404, "Session not found.")
        return session

    async def deactivate(self):
        await self.db_update_fields(is_deactivated=True)

    def get_access_token(self):
        access_token = AccessToken({"sub": str(self.user_id), "sid": str(self.id)})
        return JSONResponse({"access_token": access_token.to_jwt()}, status_code=201)
