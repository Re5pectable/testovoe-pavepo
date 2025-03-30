from pydantic import BaseModel
from ...db import RepositoryMixin, OrmSession
from uuid import UUID
from datetime import datetime
from ...adapters.token import AccessToken


class Session(BaseModel, RepositoryMixin):

    id: UUID
    user_id: UUID
    expires_at: datetime
    ip: str
    user_agent: dict
    is_deactivated: bool

    class Meta:
        orm_model = OrmSession
        
    @property
    def is_valid(self):
        if self.is_deactivated:
            return False
        if self.expires_at < datetime.now():
            return False
        return True
    
    async def deactivate(self):
        await self.db_update_fields(is_deactivated=True)
