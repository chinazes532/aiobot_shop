from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, func


async def increment_referral_count(tg_id):
    async with async_session() as session:
        async with session.begin():

            result = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = result.scalars().first()
            if not user:
                print("User  not found")
                return

            user.ref_count += 1
            session.add(user)
            await session.commit()


async def increase_user_balance(tg_id: int, amount):
    async with async_session() as session:
        async with session.begin():
            # Получаем пользователя по tg_id
            result = await session.execute(select(User).where(User.tg_id == tg_id))
            user = result.scalars().first()

            if user:
                # Прибавляем значение к балансу
                user.balance += amount

                # Сохраняем изменения в базе данных
                session.add(user)
                await session.commit()
                return True  # Успешно обновлено
            else:
                return False  # Пользователь не найден
