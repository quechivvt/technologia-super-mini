from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from sqlalchemy import select # type: ignore
from app.models.brand import Brand

class BrandRepository:

    async def find_by_id(
        self,
        db: AsyncSession,
        brand_id: int,
    ) -> Brand | None:
        stmt = (
            select(Brand)
            .where(Brand.brand_id == brand_id)
        )

        result = await db.execute(stmt)

        return result.scalar_one_or_none()

