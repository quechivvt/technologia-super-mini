from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from app.database import get_db
from decimal import Decimal
from app.schemas.product_schema import ProductCreateRequest, ProductUpdateRequest, ProductResponse
from app.services.product_service import ProductService
from app.dependencies import get_product_service
from uuid import UUID
router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
async def get_products(
    db: AsyncSession = Depends(get_db),
    service:ProductService = Depends(get_product_service),
    page: int = 1,
    size: int = 20,
    keyword: str | None = None,
    brand_id: int | None = None,
    category_id: int | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal |None = None,  
):
    return await service.get_all(
        db,
        page,
        size,
        keyword,
        brand_id,
        category_id,
        min_price, 
        max_price, )

@router.get("/{product_id}")
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    service:ProductService = Depends(get_product_service),
    )-> ProductResponse:
    return await service.get_by_id(db,product_id)

@router.post("/",status_code=201)
async def create_product(
    product: ProductCreateRequest, 
    db: AsyncSession = Depends(get_db),
    service:ProductService = Depends(get_product_service),
    ):
    return await service.create(db,product)


@router.put("/{product_id}")
async def update_product(
    product_id: UUID, 
    product: ProductUpdateRequest, 
    db: AsyncSession = Depends(get_db),
    service:ProductService = Depends(get_product_service)):
    return await service.update(db,product_id,product)


@router.delete("/{product_id}",status_code=204)
async def delete_product(
    product_id: UUID, 
    db: AsyncSession = Depends(get_db),
    service:ProductService = Depends(get_product_service),
    ):
    await service.delete(db,product_id)