from app.database.models import async_session
from app.database.models import PromoCode
from sqlalchemy import select, update


async def update_promocode_count(id):
    async with async_session() as session:
        stmt = (
            update(PromoCode)
            .where(PromoCode.id == id)
            .values(count=PromoCode.count - 1)
        )
        await session.execute(stmt)
        await session.commit()
