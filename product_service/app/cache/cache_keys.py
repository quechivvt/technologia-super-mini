from uuid import UUID


class ProductCacheKey:

    @staticmethod
    def product(product_id: UUID) -> str:
        return f"product:{product_id}"

    @staticmethod
    def products(
        page: int,
        size: int,
        keyword: str | None = None,
        brand_id: int | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> str:

        key = [
            "products",
            f"page={page}",
            f"size={size}",
        ]

        if keyword:
            key.append(f"keyword={keyword}")

        if brand_id:
            key.append(f"brand={brand_id}")

        if category_id:
            key.append(f"category={category_id}")

        if min_price is not None:
            key.append(f"min={min_price}")

        if max_price is not None:
            key.append(f"max={max_price}")

        return ":".join(key)

    @staticmethod
    def products_pattern() -> str:
        return "products:*"