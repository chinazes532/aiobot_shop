from aiogram import Bot
from aiogram.types import Message

from app.database.requests.user.add import set_user
from app.database.requests.user.select import check_referral
from app.database.requests.user.update import increment_referral_count
from app.database.requests.text.select import get_text

from config import BOT_USERNAME

import app.keyboards.builder as bkb


async def start_user(
        message: Message, tg_id, current_time,
        bot: Bot, ref_link
    ):
    text_1 = await get_text(1)

    user_registered = await set_user(
        tg_id=tg_id,
        first_name=message.from_user.first_name,
        ref_link=f"https://t.me/{BOT_USERNAME}?start={tg_id}",
        invited_by=None,
        ref_count=0,
        balance=0,
        date=current_time
    )

    if user_registered:
        if ref_link:
            invited_by = await check_referral(int(ref_link))
            if invited_by:
                await set_user(
                    tg_id=tg_id,
                    first_name=message.from_user.first_name,
                    ref_link=f"https://t.me/{BOT_USERNAME}?start={tg_id}",
                    invited_by=invited_by,
                    ref_count=0,
                    balance=0,
                    date=current_time
                )

                await bot.send_message(
                    chat_id=tg_id,
                    text=text_1.text,
                    reply_markup=await bkb.user_panel()
                )

                await bot.send_message(
                    chat_id=invited_by,
                    text=f"Пользователь {tg_id} перешел по вашей реферальной ссылке"
                )

                await increment_referral_count(invited_by)
            else:
                await bot.send_message(
                    chat_id=tg_id,
                    text=text_1.text,
                    reply_markup=await bkb.user_panel()
                )
        else:
            await bot.send_message(
                chat_id=tg_id,
                text=text_1.text,
                reply_markup=await bkb.user_panel()
            )
    else:
        await bot.send_message(
            chat_id=tg_id,
            text=text_1.text,
            reply_markup=await bkb.user_panel()
        )