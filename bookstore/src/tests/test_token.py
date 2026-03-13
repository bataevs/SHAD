import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_token(client: AsyncClient, created_seller: dict, seller_data: dict):
    resp = await client.post(
        "/api/v1/token",
        json={"email": seller_data["e_mail"], "password": seller_data["password"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_token_wrong_password(client: AsyncClient, created_seller: dict, seller_data: dict):
    resp = await client.post(
        "/api/v1/token",
        json={"email": seller_data["e_mail"], "password": "wrongpassword"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_token_wrong_email(client: AsyncClient):
    resp = await client.post(
        "/api/v1/token",
        json={"email": "nonexistent@email.com", "password": "anypassword"},
    )
    assert resp.status_code == 401
