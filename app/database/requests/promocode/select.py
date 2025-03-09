from app.database.models import async_session
from app.database.models import PromoCode
from sqlalchemy import select


async def get_promocode_by_name(name):
    async with async_session() as session:
        promocode = await session.scalar(select(PromoCode).where(PromoCode.name == name))
        return promocode
