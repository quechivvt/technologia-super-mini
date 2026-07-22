from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from sqlalchemy import select # type: ignore
from app.models.category import Category

class CategoryRepository:
    async def find_by_id(self,db:AsyncSession,category_id:int)->Category:
        stmt = (select(Category)
            .where(Category.category_id == category_id))
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
        
