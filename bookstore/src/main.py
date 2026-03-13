from fastapi import FastAPI

from src.configurations.database import Base, engine
from src.routers.books import router as books_router
from src.routers.sellers import router as sellers_router
from src.routers.token import router as token_router

app = FastAPI(title="Bookstore API", version="1.0.0")

app.include_router(sellers_router)
app.include_router(books_router)
app.include_router(token_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Bookstore API is running"}
