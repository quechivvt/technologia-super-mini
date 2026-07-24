from decimal import Decimal
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.product_cache_repository import ProductCacheRepository
from app.core.exceptions import ApiException
from app.models.product import Product
from app.repositories.brand_repository import BrandRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.event.publisher import RedisPublisher
from app.event.events import ProductEvent
from app.event.channels import Channels
from app.schemas.base_response import PageResponse
from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
)


class ProductService:

    def __init__(
        self,
        publisher: RedisPublisher,
        product_repository: ProductRepository,
        product_cache_repository: ProductCacheRepository,
        brand_repository: BrandRepository,
        category_repository: CategoryRepository,
    ):
        self.product_repository = product_repository
        self.product_cache_repository = product_cache_repository
        self.brand_repository = brand_repository
        self.category_repository = category_repository
        self.publisher = publisher

    async def get_by_id(
        self,
        db: AsyncSession,
        product_id: UUID,
    ) -> ProductResponse:

        cached = await self.product_cache_repository.get_product(product_id)

        if cached:
            return cached

        product = await self.product_repository.find_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ApiException(404, "Product not found!")

        response = ProductResponse.model_validate(product)

        await self.product_cache_repository.set_product(response)

        return response

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

        cached = await self.product_cache_repository.get_products(
            page=page,
            size=size,
            keyword=keyword,
            brand_id=brand_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
        )

        if cached:
            return cached

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

        response = PageResponse[ProductResponse](
            page=page,
            size=size,
            total=total,
            items=[
                ProductResponse.model_validate(product)
                for product in products
            ],
        )

        await self.product_cache_repository.set_products(
            response=response,
            keyword=keyword,
            brand_id=brand_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
        )

        return response

    async def create(
        self,
        db: AsyncSession,
        request: ProductCreateRequest,
    ) -> ProductResponse:

        try:

            brand = await self.brand_repository.find_by_id(
                db,
                request.brand_id,
            )

            if brand is None:
                raise ApiException(404, "Brand not found")

            category = await self.category_repository.find_by_id(
                db,
                request.category_id,
            )

            if category is None:
                raise ApiException(404, "Category not found")

            existing = await self.product_repository.find_by_name(
                db,
                request.name,
            )

            if existing:
                raise ApiException(409, "Product already exists")

            display_price = min(
                variant.price for variant in request.variants
            )

            total_stock = sum(
                variant.stock for variant in request.variants
            )

            product = Product(
                name=request.name,
                description=request.description,
                brand_id=request.brand_id,
                category_id=request.category_id,
                display_price=display_price,
                total_stock=total_stock,
            )

            product = await self.product_repository.create(
                db,
                product,
            )

            await self.publisher.publish(
                Channels.PRODUCT,
                {
                    "event": ProductEvent.CREATED,
                    "product_id": str(product.product_id),
                    "name": product.name,
                },
            )
            product = await self.product_repository.find_by_id(
                db,
                product.product_id,
            )

            response = ProductResponse.model_validate(product)

            await self.product_cache_repository.set_product(response)

            await self.product_cache_repository.delete_product_pages()

            return response

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
                raise ApiException(404, "Product not found!")

            brand = await self.brand_repository.find_by_id(
                db,
                request.brand_id,
            )

            if brand is None:
                raise ApiException(404, "Brand not found")

            category = await self.category_repository.find_by_id(
                db,
                request.category_id,
            )

            if category is None:
                raise ApiException(404, "Category not found")

            product.name = request.name
            product.description = request.description
            product.brand_id = request.brand_id
            product.category_id = request.category_id

            product = await self.product_repository.update(
                db,
                product,
            )

            response = ProductResponse.model_validate(product)

            await self.publisher.publish(
                Channels.PRODUCT,
                {
                    "event": ProductEvent.UPDATED,
                    "product_id": str(product.product_id),
                    "name": product.name,
                },
            )

            await self.product_cache_repository.set_product(response)

            await self.product_cache_repository.delete_product_pages()

            return response

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
    ) -> None:

        product = await self.product_repository.find_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ApiException(404, "Product not found!")

        await self.product_repository.delete(
            db,
            product,
        )

        await self.product_cache_repository.delete_product(
            product_id,
        )

        await self.product_cache_repository.delete_product_pages()

        await self.publisher.publish(
            Channels.PRODUCT,
            {
                "event": ProductEvent.DELETED,
                "product_id": str(product_id),
            },
        )