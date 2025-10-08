import asyncio
import os
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.database import get_engine, get_session, get_session_maker
from app.main import create_app
from app.models import Base


@pytest.fixture(scope="session")
def engine(tmp_path_factory: pytest.TempPathFactory) -> Iterator[AsyncEngine]:
    db_path = tmp_path_factory.mktemp("db") / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path}"
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_maker.cache_clear()

    engine = create_async_engine(os.environ["DATABASE_URL"], future=True)

    async def init_models() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_models())

    yield engine

    asyncio.run(engine.dispose())
    get_engine.cache_clear()
    get_session_maker.cache_clear()
    get_settings.cache_clear()


@pytest.fixture()
def client(engine: AsyncEngine) -> Iterator[TestClient]:
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    app = create_app()

    async def override_get_session():
        async with session_factory() as session:
            yield session

    def override_get_engine() -> AsyncEngine:
        return engine

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_engine] = override_get_engine

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_session, None)
    app.dependency_overrides.pop(get_engine, None)
