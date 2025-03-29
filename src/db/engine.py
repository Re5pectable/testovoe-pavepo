import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

HOST: str = os.getenv("DB_HOST")
DATABASE: str = os.getenv("DB_NAME")
USER: str = os.getenv("DB_USERNAME")
PASSWORD: str = os.getenv("DB_PASSWORD")

URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

engine = create_async_engine(URL)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency
async def get_session() -> AsyncSession: # type: ignore
    async with Session() as session:
        yield session


class UnitOfWork:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                await self.session.commit()
        except IntegrityError as e:
            detail = str(e.orig.args[0])
            raise ValueError(detail.split("\n")[1])
        finally:
            await self.session.rollback()
            await self.session.close()
