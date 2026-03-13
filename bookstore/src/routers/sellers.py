from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.models.sellers import Seller
from src.schemas.sellers import SellerCreate, SellerDetailResponse, SellerResponse, SellerUpdate
from src.services.auth import get_current_seller
from src.services.sellers import (
    create_seller,
    delete_seller,
    get_all_sellers,
    get_seller_by_id,
    update_seller,
)

router = APIRouter(prefix="/api/v1/seller", tags=["sellers"])


@router.post("/", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
async def register_seller(
    data: SellerCreate,
    session: AsyncSession = Depends(get_async_session),
):
    seller = await create_seller(session, data)
    return seller


@router.get("/", response_model=list[SellerResponse])
async def list_sellers(session: AsyncSession = Depends(get_async_session)):
    sellers = await get_all_sellers(session)
    return sellers


@router.get("/{seller_id}", response_model=SellerDetailResponse)
async def get_seller(
    seller_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_seller: Seller = Depends(get_current_seller),
):
    seller = await get_seller_by_id(session, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    return seller


@router.put("/{seller_id}", response_model=SellerResponse)
async def update_seller_info(
    seller_id: int,
    data: SellerUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    seller = await get_seller_by_id(session, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    return await update_seller(session, seller, data)


@router.delete("/{seller_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_seller(
    seller_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    seller = await get_seller_by_id(session, seller_id)
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
    await delete_seller(session, seller)
