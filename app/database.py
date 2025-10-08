from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import get_settings


def create_engine(database_url: str | None = None) -> AsyncEngine:
    settings = get_settings()
    url = database_url or str(settings.database_url)
    return create_async_engine(url, future=True, echo=False)


@lru_cache()
def get_engine() -> AsyncEngine:
    return create_engine()


@lru_cache()
def get_session_maker() -> async_sessionmaker[AsyncSession]:
    engine = get_engine()
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_maker = get_session_maker()
    async with session_maker() as session:
        yield session
