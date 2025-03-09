from aiogram import Bot

from app.database.requests.user.select import get_user
from app.database.requests.percent.select import get_percent
from app.database.requests.user.update import increase_user_balance


async def check_referral(tg_id, price):
    first_percent = await get_percent(1)
    second_percent = await get_percent(2)
    user = await get_user(tg_id)
    referral_id = user.invited_by
    referral = await get_user(referral_id)
    second_referral_id = await get_user(referral.invited_by)
    second_referral = await get_user(second_referral_id)

    if referral:
        total = price * (first_percent.count / 100)
        await increase_user_balance(referral_id, total)

    if second_referral:
        total = price * (second_percent.count / 100)
        await increase_user_balance(second_referral_id, total)

