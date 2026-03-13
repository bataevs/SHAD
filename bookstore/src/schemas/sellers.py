from pydantic import BaseModel, EmailStr

from src.schemas.books import BookResponse


class SellerCreate(BaseModel):
    first_name: str
    last_name: str
    e_mail: EmailStr
    password: str


class SellerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    e_mail: EmailStr | None = None


class SellerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    e_mail: str

    model_config = {"from_attributes": True}


class SellerDetailResponse(SellerResponse):
    books: list[BookResponse] = []
