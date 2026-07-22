from sqlalchemy.orm import Mapped, mapped_column # type: ignore

from app.database import Base

class Brand(Base):
    __tablename__ = "brands"

    brand_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
