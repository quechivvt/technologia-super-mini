from sqlalchemy.exc import IntegrityError # type: ignore
from uuid import UUID
from decimal import Decimal
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession  # type: ignore

from app.exceptions import ApiException
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse,
)
from app.schemas.base_response import PageResponse

class ProductService:
    def __init__(
        self, 
        product_repository: ProductRepository,
        brand_repository : BrandRepository,
        category_repository : CategoryRepository,
        ):
        self.product_repository = product_repository
        self.brand_repository = brand_repository
        self.category_repository = category_repository


    async def get_by_id(self, db: AsyncSession, product_id: UUID,) -> ProductResponse:

        product = await self.product_repository.find_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ApiException(404,"Product not found!")

        return ProductResponse.model_validate(product)
    
    async def get_all(
        self,
        db: AsyncSession,
        page: int,
        size: int,
        keyword: str | None,
        brand_id: int | None,
        category_id: int | None,
        min_price: Decimal | None,
        max_price: Decimal | None,
    ) -> PageResponse[ProductResponse]:
        
        products, total = await self.product_repository.find_all(
            db=db,
            page=page,
            size=size,
            keyword=keyword,
            brand_id=brand_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
        )

        return PageResponse(
            page=page,
            size=size,
            total=total,
            items=[
                ProductResponse.model_validate(product)
                for product in products
            ]
        )
    
    async def create(
        self,
        db: AsyncSession,
        request: ProductCreateRequest,
    ) -> ProductResponse:
        try:
            display_price = min(variant.price for variant in request.variants)
            total_stock = sum(variant.stock for variant in request.variants)
            brand = await self.brand_repository.find_by_id(db,request.brand_id)
            if brand is None:
                raise ApiException(404, "Brand not found")

            category = await self.category_repository.find_by_id(db,request.category_id)
            if category is None:
                raise ApiException(404, "Category not found")

            existing = await self.product_repository.find_by_name(db,request.name)
            if existing:
                raise ApiException(409, "Product already exists")

            product = Product(
                name=request.name,
                description=request.description,
                brand_id=request.brand_id,
                category_id=request.category_id,
                display_price = display_price,
                total_stock = total_stock
            )

            product = await self.product_repository.create(
                db,
                product,
            )

            return ProductResponse.model_validate(product)
        except IntegrityError:
            await db.rollback()
            raise ApiException(409, "Product already exists")
        except Exception:
            await db.rollback()
            raise
    
    async def update(
        self,
        db: AsyncSession,
        product_id: UUID,
        request: ProductUpdateRequest,
    ) -> ProductResponse:
        try:
            product = await self.product_repository.find_by_id(
                db,
                product_id,
            )

            if product is None:
                raise ApiException(404,"Product not found!")

            product.name = request.name
            product.description = request.description
            brand = await self.brand_repository.find_by_id(db,request.brand_id)
            if brand is None:
                raise ApiException(404, "Brand not found")

            category = await self.category_repository.find_by_id(db,request.category_id)
            if category is None:
                raise ApiException(404, "Category not found")
            product.brand_id = request.brand_id
            product.category_id = request.category_id

            product = await self.product_repository.update(
                db,
                product,
            )

            return ProductResponse.model_validate(product)
        except IntegrityError:
            await db.rollback()
            raise ApiException(409, "Product already exists")
        except Exception:
            await db.rollback()
            raise
    
    async def delete(
        self,
        db: AsyncSession,
        product_id: UUID,
    )-> None:

        product = await self.product_repository.find_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ApiException(404,"Product not found!")

        await self.product_repository.delete(
            db,
            product,
        )



