from ...db import UnitOfWork, OrmUser, OrmUserExternalOauth, OrmSession
from sqlalchemy import select, update


async def get_user_by_external_id(external_id: str) -> OrmUser | None:
    async with UnitOfWork(autocommit=False) as session:
        stmt = (
            select(OrmUser)
            .select_from(OrmUser)
            .join(OrmUserExternalOauth, OrmUserExternalOauth.user_id == OrmUser.id)
            .where(OrmUserExternalOauth.external_id == external_id, OrmUser.is_deleted.is_not(True))
        )
        q = await session.execute(stmt)
        return q.scalars().first()


async def create_user(
    email: str,
    name: str,
    surname: str,
    external_id: str | None = None,
) -> OrmUser:
    async with UnitOfWork() as session:
        user = OrmUser(email=email, name=name, surname=surname)
        session.add(user)
        await session.flush()

        if external_id:
            session.add(OrmUserExternalOauth(user_id=user.id, external_id=external_id))

    return user


async def deactivate_all_sessions(user_id):
    async with UnitOfWork() as session:
        stmt = (
            update(OrmSession)
            .where(
                OrmSession.user_id == user_id, OrmSession.is_deactivated.is_not(True)
            )
            .values(is_deactivated=True)
        )
        await session.execute(stmt)
