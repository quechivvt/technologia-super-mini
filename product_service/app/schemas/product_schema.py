from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from uuid import UUID
from app.schemas.product_variant_schema import ProductVariantCreateRequest, ProductVariantResponse


class ProductCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    brand_id: int
    category_id: int
    variants: list[ProductVariantCreateRequest]  

class ProductUpdateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = None
    description: str | None = None
    brand_id: int | None = None
    category_id: int | None = None

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_id: UUID
    name: str
    description: str
    brand_id: int
    category_id: int
    total_stock: int
    display_price: Decimal
    created_at: datetime
    updated_at: datetime | None
    variants: list[ProductVariantResponse]
