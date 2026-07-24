from uuid import UUID

from app.cache.cache_keys import ProductCacheKey
from app.cache.cache_repository import CacheRepository
from app.schemas.base_response import PageResponse
from app.schemas.product_schema import ProductResponse


class ProductCacheRepository:

    def __init__(self, cache: CacheRepository):
        self.cache = cache

    async def get_product(
        self,
        product_id: UUID,
    ) -> ProductResponse | None:

        return await self.cache.get(
            ProductCacheKey.product(product_id),
            ProductResponse,
        )

    async def set_product(
        self,
        product: ProductResponse,
    ) -> None:

        await self.cache.set(
            ProductCacheKey.product(product.product_id),
            product,
        )

    async def delete_product(
        self,
        product_id: UUID,
    ) -> None:

        await self.cache.delete(
            ProductCacheKey.product(product_id),
        )

    async def get_products(
        self,
        page: int,
        size: int,
        keyword: str | None = None,
        brand_id: int | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> PageResponse[ProductResponse] | None:

        return await self.cache.get(
            ProductCacheKey.products(
                page=page,
                size=size,
                keyword=keyword,
                brand_id=brand_id,
                category_id=category_id,
                min_price=min_price,
                max_price=max_price,
            ),
            PageResponse[ProductResponse],
        )

    async def set_products(
        self,
        response: PageResponse[ProductResponse],
        keyword: str | None = None,
        brand_id: UUID | None = None,
        category_id: UUID | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> None:

        await self.cache.set(
            ProductCacheKey.products(
                page=response.page,
                size=response.size,
                keyword=keyword,
                brand_id=brand_id,
                category_id=category_id,
                min_price=min_price,
                max_price=max_price,
            ),
            response,
        )

    async def delete_product_pages(self) -> None:

        await self.cache.delete_pattern(
            ProductCacheKey.products_pattern()
        )