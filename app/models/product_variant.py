from sqlalchemy.orm import Mapped, mapped_column, relationship # type: ignore
from sqlalchemy import ForeignKey, Numeric # type: ignore
from uuid import UUID
from decimal import Decimal

from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.product import Product

class ProductVariant(Base):
    __tablename__ = "product_variants"

    variant_id: Mapped[str] = mapped_column(primary_key=True)
    color: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False, default=0)
    storage: Mapped[str] = mapped_column(nullable=False)
    price_after_discount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2),nullable=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.product_id"),nullable=False)
    product: Mapped["Product"] = relationship("Product", back_populates="variants")
