from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select


async def set_user(tg_id, first_name, ref_link, invited_by, ref_count, date, balance):
    async with async_session() as session:
        async with session.begin():
            # Проверяем, существует ли пользователь
            result = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = result.scalars().first()

            if user:
                # Пользователь уже зарегистрирован
                if user.ref_count == 0 and not user.invited_by:
                    # Проверяем, что пользователь не перешел по своей собственной реферальной ссылке
                    if invited_by and invited_by != tg_id:
                        user.invited_by = invited_by
                        session.add(user)
                        await session.commit()
                        return True
                    else:
                        return False
                else:
                    # Пользователь уже перешел по реферальной ссылке или уже пригласил других
                    return False
            else:
                # Создаем нового пользователя
                new_user = User(
                    tg_id=tg_id,
                    first_name=first_name,
                    ref_link=ref_link,
                    invited_by=invited_by,
                    ref_count=ref_count,
                    date=date,
                    balance=balance
                )
                session.add(new_user)
                await session.commit()
                return True


