from app.database.models import async_session
from app.database.models import Category
from sqlalchemy import select


async def get_categories():
    async with async_session() as session:
        categories = await session.scalars(select(Category))
        return categories


async def get_category(id):
    async with async_session() as session:
        category = await session.scalar(select(Category).where(Category.id == id))
        return category
