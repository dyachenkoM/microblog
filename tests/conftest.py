import pytest
from httpx import AsyncClient, ASGITransport
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
test_engine = create_async_engine(TEST_DB_URL, poolclass=NullPool, echo=True)


@pytest.fixture(scope="session", autouse=True)
async def db_session():
    """Фикстура для управления жизненным циклом БД"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def prepare_user():
    """Создаем тестового пользователя один раз для всех тестов"""
    async_session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        user = User(name="TestUser")
        session.add(user)
        await session.flush()

        key = UserKey(api_key="test", user_id=user.id)
        session.add(key)
        await session.commit()
        yield


@pytest.fixture(scope="function")
async def client(db_session, prepare_user):
    """Фикстура клиента с переиспользованием данных между тестами"""

    async def override_session():
        async_session = async_sessionmaker(
            bind=test_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
        async with async_session() as session:
            yield session

    test_app.dependency_overrides[db_helper.session_getter] = override_session

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    test_app.dependency_overrides.clear()
