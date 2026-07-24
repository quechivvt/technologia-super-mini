from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime
from uuid import UUID

class ProductVariantCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    color: str
    price: Decimal
    stock: int
    storage: str

class ProductVariantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    variant_id: str
    product_id: UUID
    color: str
    price: Decimal
    stock: int
    storage: str