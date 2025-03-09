from app.database.models import async_session
from app.database.models import Text
from sqlalchemy import select


async def get_text(id):
    async with async_session() as session:
        text = await session.scalar(select(Text).where(Text.id == id))
        return text
