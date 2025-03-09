from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.text.select import get_text


async def user_panel():
    kb = InlineKeyboardBuilder()

    text_2 = await get_text(2)
    text_3 = await get_text(3)
    text_4 = await get_text(4)
    text_5 = await get_text(5)

    kb.row(InlineKeyboardButton(text=text_2.text, callback_data="products"))
    kb.row(InlineKeyboardButton(text=text_3.text, callback_data="referral"))
    kb.row(InlineKeyboardButton(text=text_4.text, url=text_5.text))

    return kb.as_markup()


async def user_back_to_menu():
    kb = InlineKeyboardBuilder()

    text_8 = await get_text(8)

    kb.row(InlineKeyboardButton(text=text_8.text, callback_data="user_back"))

    return kb.as_markup()