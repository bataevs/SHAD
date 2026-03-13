from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import Book
from src.schemas.books import BookCreate, BookUpdate


async def create_book(session: AsyncSession, data: BookCreate) -> Book:
    book = Book(**data.model_dump())
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def get_all_books(session: AsyncSession) -> list[Book]:
    result = await session.execute(select(Book))
    return result.scalars().all()


async def get_book_by_id(session: AsyncSession, book_id: int) -> Book | None:
    result = await session.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(session: AsyncSession, book: Book, data: BookUpdate) -> Book:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    await session.commit()
    await session.refresh(book)
    return book


async def delete_book(session: AsyncSession, book: Book) -> None:
    await session.delete(book)
    await session.commit()
