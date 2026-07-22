from sqlalchemy import ForeignKey # type: ignore
from sqlalchemy.orm import Mapped, mapped_column # type: ignore

from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)