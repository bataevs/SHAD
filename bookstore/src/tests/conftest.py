import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from src.configurations.database import Base, get_async_session
from src.configurations.settings import settings
from src.main import app

# Создаем тестовый движок
test_engine = create_async_engine(
    settings.test_database_url, 
    echo=False,
    pool_size=5,  
    max_overflow=10
)
test_session_factory = async_sessionmaker(
    test_engine, 
    expire_on_commit=False,
    class_=AsyncSession
)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_db():
    async with test_engine.connect() as conn:
        # Начинаем транзакцию для DDL
        await conn.execute(text("COMMIT"))  
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield
    async with test_engine.connect() as conn:
        await conn.execute(text("COMMIT"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


@pytest_asyncio.fixture()
async def db_session(setup_db):
    async with test_session_factory() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture()
async def client(db_session) -> AsyncClient:
    
    async def override_get_async_session():
        yield db_session
    
    app.dependency_overrides[get_async_session] = override_get_async_session
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as c:
        yield c
    
    app.dependency_overrides.clear()


@pytest.fixture()
def seller_data():
    return {
        "first_name": "Ivan",
        "last_name": "Petrov",
        "e_mail": "ivan@example.com",
        "password": "secret123",
    }


@pytest_asyncio.fixture()
async def created_seller(client: AsyncClient, seller_data: dict):
    resp = await client.post("/api/v1/seller/", json=seller_data)
    assert resp.status_code == 201
    return resp.json()


@pytest_asyncio.fixture()
async def auth_token(client: AsyncClient, created_seller: dict, seller_data: dict):
    resp = await client.post(
        "/api/v1/token",
        json={"email": seller_data["e_mail"], "password": seller_data["password"]},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


@pytest.fixture()
def auth_headers(auth_token: str):
    return {"Authorization": f"Bearer {auth_token}"}