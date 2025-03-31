import os
from datetime import datetime
from uuid import UUID, uuid4

import aiofiles
from fastapi import UploadFile, HTTPException
from pydantic import BaseModel, ConfigDict

from ...config import MEDIA_PATH, ALLOWED_EXTENTIONS
from ...db import OrmFiles, RepositoryMixin


class Media(BaseModel, RepositoryMixin):
    id: UUID
    created_at: datetime
    name: str
    path: str
    user_id: UUID

    model_config = ConfigDict(from_attributes=True)

    class Meta:
        orm_model = OrmFiles

    @classmethod
    async def create(cls, user_id, file: UploadFile):
        extention = file.filename.split(".")[-1]
        if extention not in ALLOWED_EXTENTIONS:
            raise HTTPException(403, "Forbidden extention.")
        
        id = uuid4()
        save_path = MEDIA_PATH + f"/{id}_" + file.filename
        async with aiofiles.open(save_path, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
                
        media = cls(
            id=id,
            created_at=datetime.now(),
            user_id=user_id,
            name=file.filename,
            path=save_path,
        )
        try:
            await media.db_create()
        except Exception as e:
            os.remove(save_path)
            raise e
