from app.database.models import async_session
from app.database.models import Percent
from sqlalchemy import select


async def get_percent(id):
    async with async_session() as session:
        percent = await session.scalar(select(Percent).where(Percent.id == id))
        return percent
