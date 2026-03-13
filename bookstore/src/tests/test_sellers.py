import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_seller(client: AsyncClient):
    payload = {
        "first_name": "Anna",
        "last_name": "Sidorova",
        "e_mail": "anna@test.com",
        "password": "pass123",
    }
    resp = await client.post("/api/v1/seller/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["first_name"] == "Anna"
    assert data["e_mail"] == "anna@test.com"
    assert "password" not in data
    assert "id" in data


@pytest.mark.asyncio
async def test_list_sellers(client: AsyncClient, created_seller: dict):
    resp = await client.get("/api/v1/seller/")
    assert resp.status_code == 200
    sellers = resp.json()
    assert isinstance(sellers, list)
    assert len(sellers) >= 1
    # password must not be in response
    for seller in sellers:
        assert "password" not in seller


@pytest.mark.asyncio
async def test_get_seller_detail(client: AsyncClient, created_seller: dict, auth_headers: dict):
    seller_id = created_seller["id"]
    resp = await client.get(f"/api/v1/seller/{seller_id}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == seller_id
    assert "password" not in data
    assert "books" in data


@pytest.mark.asyncio
async def test_get_seller_detail_unauthorized(client: AsyncClient, created_seller: dict):
    seller_id = created_seller["id"]
    resp = await client.get(f"/api/v1/seller/{seller_id}")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_seller_not_found(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/api/v1/seller/99999", headers=auth_headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_seller(client: AsyncClient, created_seller: dict):
    seller_id = created_seller["id"]
    resp = await client.put(
        f"/api/v1/seller/{seller_id}",
        json={"first_name": "UpdatedName"},
    )
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "UpdatedName"
    assert "password" not in resp.json()


@pytest.mark.asyncio
async def test_delete_seller(client: AsyncClient, created_seller: dict):
    seller_id = created_seller["id"]
    resp = await client.delete(f"/api/v1/seller/{seller_id}")
    assert resp.status_code == 204

    # Verify deleted
    resp2 = await client.get("/api/v1/seller/")
    assert all(s["id"] != seller_id for s in resp2.json())
