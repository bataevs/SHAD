from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.models.sellers import Seller
from src.schemas.books import BookCreate, BookResponse, BookUpdate
from src.services.auth import get_current_seller
from src.services.books import (
    create_book,
    delete_book,
    get_all_books,
    get_book_by_id,
    update_book,
)

router = APIRouter(prefix="/api/v1/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
    data: BookCreate,
    session: AsyncSession = Depends(get_async_session),
    current_seller: Seller = Depends(get_current_seller),
):
    book = await create_book(session, data)
    return book


@router.get("/", response_model=list[BookResponse])
async def list_books(session: AsyncSession = Depends(get_async_session)):
    return await get_all_books(session)


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    book = await get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
async def edit_book(
    book_id: int,
    data: BookUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_seller: Seller = Depends(get_current_seller),
):
    book = await get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return await update_book(session, book, data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(book_id: int, session: AsyncSession = Depends(get_async_session)):
    book = await get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await delete_book(session, book)
