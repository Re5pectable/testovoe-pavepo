from pydantic import TypeAdapter, ConfigDict
from sqlalchemy import delete, select, update

from .engine import UnitOfWork


class RepositoryMixin:

    async def db_create(self):
        ignore_fields = (
            self.Meta.ignore_fields if hasattr(self.Meta, "ignore_fields") else {}
        )
        obj = self.Meta.orm_model(**self.model_dump(exclude=ignore_fields))
        async with UnitOfWork() as session:
            session.add(obj)
        return obj.id

    async def db_update(self) -> None:
        orm_cls = self.Meta.orm_model
        ignore_fields = (
            self.Meta.ignore_fields if hasattr(self.Meta, "ignore_fields") else {}
        )
        stmt = (
            update(orm_cls)
            .where(orm_cls.id == self.id)
            .values(**self.model_dump(exclude=ignore_fields))
        )
        async with UnitOfWork() as session:
            await session.execute(stmt)

    async def db_update_fields(self, **kwargs):
        orm_model = self.Meta.orm_model
        async with UnitOfWork() as session:
            stmt = update(orm_model).where(orm_model.id == self.id).values(**kwargs)
            await session.execute(stmt)

    async def db_delete(self) -> None:
        orm_cls = self.Meta.orm_model
        if getattr(orm_cls, "is_deleted"):
            stmt = update(orm_cls).where(orm_cls.id == self.id).values(is_deleted=True)
        else:
            stmt = delete(orm_cls).where(orm_cls.id == self.id)
        async with UnitOfWork() as session:
            await session.execute(stmt)

    @classmethod
    async def _db_get(cls, limit=None, **kwargs):
        orm_cls = cls.Meta.orm_model
        stmt = select(orm_cls).filter_by(**kwargs)
        if limit:
            stmt = stmt.limit(limit)
        if hasattr(orm_cls, "is_deleted"):
            stmt = stmt.where(orm_cls.is_deleted.is_not(True))
        if hasattr(orm_cls, "created_at"):
            stmt = stmt.order_by(orm_cls.created_at.desc())
        async with UnitOfWork() as session:
            return await session.execute(stmt)

    @classmethod
    async def db_get_or_none(cls, **kwargs):
        q = await cls._db_get(limit=1, **kwargs)
        q_first = q.scalars().first()
        if q_first:
            return TypeAdapter(cls).validate_python(q_first)
        return None

    @classmethod
    async def db_get_many(cls, **kwargs):
        q = await cls._db_get(**kwargs)
        q_all = q.scalars().all()
        return TypeAdapter(list[cls]).validate_python(q_all)
