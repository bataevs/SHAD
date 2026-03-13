from pydantic import BaseModel, field_validator


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    count_pages: int
    seller_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    count_pages: int | None = None
    seller_id: int | None = None


class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        if v < 1900 or v > 2025:
            raise ValueError("Year must be between 1900 and 2025")
        return v
