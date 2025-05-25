import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool

from core import db_helper
from core.models import Base, User, UserKey
from main import main_app as test_app


TEST_DB_URL = "postgresql+asyncpg://user:password@localhost:5432/test_db"
test_engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)


@pytest.fixture(scope="function")
async def client():
    """Фикстура клиента FastAPI, с переопределённой зависимостью сессии"""

    async def override_session():
        async_session = async_sessionmaker(
            bind=test_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        async with async_session() as session:
            await session.execute(text("TRUNCATE users_keys, users RESTART IDENTITY CASCADE"))
            await session.commit()

            user = User(name="TestUser")
            session.add(user)
            await session.flush()

            key = UserKey(api_key="test", user_id=user.id)
            session.add(key)

            await session.commit()
            yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    test_app.dependency_overrides[db_helper.session_getter] = override_session

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    test_app.dependency_overrides.clear()
