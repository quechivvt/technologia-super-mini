from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
from sqlalchemy import DateTime, Numeric, ForeignKey # type: ignore
from datetime import datetime
from decimal import Decimal
from uuid import uuid4,UUID

from app.database import Base
from app.enums.product_status import ProductStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product_variant import ProductVariant

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    average_rating: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime,nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    display_price: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False)
    status: Mapped[ProductStatus] = mapped_column(nullable=False, default=ProductStatus.AVAILABLE)
    total_stock: Mapped[int] = mapped_column(nullable=False, default=0)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.brand_id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"), nullable=False)
    variants: Mapped[list["ProductVariant"]] = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")