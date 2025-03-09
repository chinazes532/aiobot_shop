from app.database.models import async_session
from app.database.models import Product
from sqlalchemy import select


async def get_products_by_category_id(category_id):
    async with async_session() as session:
        products = await session.scalars(select(Product).where(Product.category_id == category_id))
        return products


async def get_product(id):
    async with async_session() as session:
        product = await session.scalar(select(Product).where(Product.id == id))
        return product
