import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode
from yookassa import Configuration

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb
from app.database.requests.text.select import get_text

from app.filters.admin_filter import AdminProtect, check_start_admin

from app.database.requests.user.add import set_user
from app.database.requests.user.update import increment_referral_count
from app.database.requests.user.select import get_user, check_referral
from app.filters.user_filter import start_user


user = Router()


Configuration.account_id = 1012748
Configuration.secret_key = "test_MbOgnH624LCJuYZwksDGxl6lDUz4oH3VLYq1tHWON4Y"


@user.message(CommandStart())
async def start_command(message: Message, bot: Bot, command: CommandObject, dialog_manager: DialogManager):
    admin = AdminProtect()
    tg_id = message.from_user.id
    ref_link = command.args
    current_time = datetime.datetime.now().strftime("%d.%m.%Y")

    if await admin(message):
        await check_start_admin(message, tg_id, current_time)

        return

    await start_user(
        message, tg_id, current_time,
        bot, ref_link
    )


@user.callback_query(F.data == "referral")
async def user_referral_info(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user = await get_user(tg_id)

    await callback.message.edit_text(f"<b>РЕФЕРАЛЬНАЯ СИСТЕМА</b>\n\n"
                                     f"<b>Ваш ID:</b> {user.tg_id}\n"
                                     f"<b>Баланс:</b> {user.balance}\n"
                                     f"<b>Вы пригласили {user.ref_count} пользователей</b>\n"
                                     f"<b>Ваша ссылка:</b> <code>{user.ref_link}</code>",
                                     reply_markup=await bkb.user_back_to_menu(),
                                     disable_web_page_preview=True)


@user.callback_query(F.data == "user_back")
async def user_back(callback: CallbackQuery):
    text_1 = await get_text(1)

    await callback.message.edit_text(text_1.text,
                                     reply_markup=await bkb.user_panel())



