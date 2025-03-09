import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from config import BOT_TOKEN

from app.handlers.user_message import user
from app.handlers.admin_message import admin
from app.handlers.buy_message import buy, buy_dialog

from app.database.models import create_db


async def main():
    print("Bot is starting...")

    await create_db()

    bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(user)
    dp.include_router(admin)
    dp.include_router(buy)
    dp.include_router(buy_dialog)

    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
