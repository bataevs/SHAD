from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.configurations.database import Base


class Seller(Base):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    e_mail: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(200))

    books: Mapped[list["Book"]] = relationship(  # noqa: F821
        "Book", back_populates="seller", cascade="all, delete-orphan"
    )
