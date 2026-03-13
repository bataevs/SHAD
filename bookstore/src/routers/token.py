from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.configurations.database import get_async_session
from src.schemas.token import Token
from src.services.auth import create_access_token
from src.services.sellers import get_seller_by_email, verify_password

router = APIRouter(prefix="/api/v1", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/token", response_model=Token)
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_async_session),
):
    seller = await get_seller_by_email(session, data.email)
    if not seller or not verify_password(data.password, seller.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    token = create_access_token(seller.id)
    return Token(access_token=token)
