from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from sqlalchemy import select, func # type: ignore
from sqlalchemy.orm import selectinload # type: ignore
from app.models.product import Product
from decimal import Decimal

class ProductRepository:

    async def find_by_id(
        self,
        db: AsyncSession,
        product_id: UUID,
    ) -> Product | None:

        

        stmt = (
            select(Product)
            .options(selectinload(Product.variants))
            .where(Product.product_id == product_id)
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()
    
    async def find_by_name(
        self,
        db: AsyncSession,
        name: str
    ):
        stmt = (
            select(Product)
            .options(selectinload(Product.variants))
            .where(Product.name == name)
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()
    
    async def find_all(
        self,
        db: AsyncSession,
        page: int = 1,
        size: int = 20,
        keyword: str | None = None,
        brand_id: int | None = None,
        category_id: int | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
    ) -> tuple[list[Product], int]:
        
        conditions = []

        if keyword:
            conditions.append(Product.name.ilike(f"%{keyword}%"))

        if brand_id is not None:
            conditions.append(Product.brand_id == brand_id)

        if category_id is not None:
            conditions.append(Product.category_id == category_id)

        if min_price is not None:
            conditions.append(Product.display_price >= min_price)

        if max_price is not None:
            conditions.append(Product.display_price <= max_price)

        stmt = (
            select(Product)
            .where(*conditions)
            .options(selectinload(Product.variants))
            .offset((page - 1) * size)
            .limit(size)
        )

        count_stmt = (
            select(func.count(Product.product_id))
            .where(*conditions)
        )

        result = await db.execute(stmt)
        products = result.scalars().all()

        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()
        return products, total

    async def create(self, db: AsyncSession, product: Product) -> Product:
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    async def update(self, db:AsyncSession, product:Product) -> Product:
        await db.commit()
        await db.refresh(product)
        return product

    async def delete(self,db: AsyncSession,product: Product) -> None:
        await db.delete(product)
        await db.commit()