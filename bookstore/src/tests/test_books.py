import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_book(client: AsyncClient, created_seller: dict, auth_headers: dict):
    payload = {
        "title": "Clean Code",
        "author": "Robert Martin",
        "year": 2008,
        "count_pages": 431,
        "seller_id": created_seller["id"],
    }
    resp = await client.post("/api/v1/books/", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Clean Code"
    assert data["seller_id"] == created_seller["id"]
    assert "id" in data


@pytest.mark.asyncio
async def test_create_book_unauthorized(client: AsyncClient, created_seller: dict):
    payload = {
        "title": "Clean Code",
        "author": "Robert Martin",
        "year": 2008,
        "count_pages": 431,
        "seller_id": created_seller["id"],
    }
    resp = await client.post("/api/v1/books/", json=payload)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_list_books(client: AsyncClient, created_seller: dict, auth_headers: dict):
    # Create a book first
    await client.post(
        "/api/v1/books/",
        json={
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "year": 1999,
            "count_pages": 352,
            "seller_id": created_seller["id"],
        },
        headers=auth_headers,
    )
    resp = await client.get("/api/v1/books/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_book(client: AsyncClient, created_seller: dict, auth_headers: dict):
    create_resp = await client.post(
        "/api/v1/books/",
        json={
            "title": "Design Patterns",
            "author": "Gang of Four",
            "year": 1994,
            "count_pages": 395,
            "seller_id": created_seller["id"],
        },
        headers=auth_headers,
    )
    book_id = create_resp.json()["id"]
    resp = await client.get(f"/api/v1/books/{book_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == book_id


@pytest.mark.asyncio
async def test_get_book_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/books/99999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_book(client: AsyncClient, created_seller: dict, auth_headers: dict):
    create_resp = await client.post(
        "/api/v1/books/",
        json={
            "title": "Old Title",
            "author": "Some Author",
            "year": 2000,
            "count_pages": 200,
            "seller_id": created_seller["id"],
        },
        headers=auth_headers,
    )
    book_id = create_resp.json()["id"]
    resp = await client.put(
        f"/api/v1/books/{book_id}",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_update_book_unauthorized(client: AsyncClient, created_seller: dict, auth_headers: dict):
    create_resp = await client.post(
        "/api/v1/books/",
        json={
            "title": "A Book",
            "author": "Author",
            "year": 2010,
            "count_pages": 100,
            "seller_id": created_seller["id"],
        },
        headers=auth_headers,
    )
    book_id = create_resp.json()["id"]
    resp = await client.put(f"/api/v1/books/{book_id}", json={"title": "Hacked"})
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_delete_book(client: AsyncClient, created_seller: dict, auth_headers: dict):
    create_resp = await client.post(
        "/api/v1/books/",
        json={
            "title": "To Delete",
            "author": "Author",
            "year": 2015,
            "count_pages": 150,
            "seller_id": created_seller["id"],
        },
        headers=auth_headers,
    )
    book_id = create_resp.json()["id"]
    resp = await client.delete(f"/api/v1/books/{book_id}")
    assert resp.status_code == 204


@pytest.mark.asyncio
async def test_seller_books_cascade_delete(
    client: AsyncClient, created_seller: dict, auth_headers: dict
):
    # Create book for seller
    book_resp = await client.post(
        "/api/v1/books/",
        json={
            "title": "Cascade Test Book",
            "author": "Author",
            "year": 2020,
            "count_pages": 300,
            "seller_id": created_seller["id"],
        },
        headers=auth_headers,
    )
    book_id = book_resp.json()["id"]

    # Delete seller
    await client.delete(f"/api/v1/seller/{created_seller['id']}")

    # Book should also be deleted
    resp = await client.get(f"/api/v1/books/{book_id}")
    assert resp.status_code == 404
