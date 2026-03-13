from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.sellers import Seller
from src.schemas.sellers import SellerCreate, SellerUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_seller(session: AsyncSession, data: SellerCreate) -> Seller:
    seller = Seller(
        first_name=data.first_name,
        last_name=data.last_name,
        e_mail=data.e_mail,
        password=hash_password(data.password),
    )
    session.add(seller)
    await session.commit()
    await session.refresh(seller)
    return seller


async def get_all_sellers(session: AsyncSession) -> list[Seller]:
    result = await session.execute(select(Seller))
    return result.scalars().all()


async def get_seller_by_id(session: AsyncSession, seller_id: int) -> Seller | None:
    result = await session.execute(
        select(Seller).where(Seller.id == seller_id).options(selectinload(Seller.books))
    )
    return result.scalar_one_or_none()


async def get_seller_by_email(session: AsyncSession, email: str) -> Seller | None:
    result = await session.execute(select(Seller).where(Seller.e_mail == email))
    return result.scalar_one_or_none()


async def update_seller(
    session: AsyncSession, seller: Seller, data: SellerUpdate
) -> Seller:
    if data.first_name is not None:
        seller.first_name = data.first_name
    if data.last_name is not None:
        seller.last_name = data.last_name
    if data.e_mail is not None:
        seller.e_mail = data.e_mail
    await session.commit()
    await session.refresh(seller)
    return seller


async def delete_seller(session: AsyncSession, seller: Seller) -> None:
    await session.delete(seller)
    await session.commit()
