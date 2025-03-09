import datetime
from typing import Any

from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from yookassa import Payment

from app.database.requests.category.select import get_category
from app.database.requests.text.select import get_text
from app.database.requests.product.select import get_product

import app.keyboards.builder as bkb
from app.filters.check_referral import check_referral

from app.states import BuySG

from app.google_sheets.parse_sheets import Sheet


sheet = Sheet()


async def on_back(callback: CallbackQuery, widget: Any, manager: DialogManager):
    await manager.back()


async def on_back_menu(callback: CallbackQuery, widget: Any, manager: DialogManager):
    text_1 = await get_text(1)
    await callback.message.answer(text_1.text,
                                  reply_markup=await bkb.user_panel())
    await manager.done()


async def on_category(callback: CallbackQuery, widget: Any,
                      manager: DialogManager, category_id):
    manager.dialog_data.update(
        category_id=category_id
    )
    await manager.next()


async def on_product(callback: CallbackQuery, widget: Any,
                     manager: DialogManager, product_id):
    manager.dialog_data.update(
        product_id=product_id
    )
    manager.dialog_data.update(tg_id=callback.from_user.id)
    await manager.next()


async def on_info(callback: CallbackQuery, widget: Any,
                  manager: DialogManager):
    await manager.next()


async def on_no_promocode(callback: CallbackQuery, widget: Any,
                          manager: DialogManager):
    product_id = manager.dialog_data.get("product_id")
    product = await get_product(int(product_id))
    manager.dialog_data.update(price=product.price)
    await manager.switch_to(BuySG.payment)


async def on_check_payment(callback: CallbackQuery, widget: Any,
                           manager: DialogManager):
    payment_id = manager.dialog_data.get("payment_id")
    payment = Payment.find_one(payment_id)
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")

    product_id = manager.dialog_data.get("product_id")
    product = await get_product(int(product_id))
    price = manager.dialog_data.get("price")

    text_16 = await get_text(16)
    text_17 = await get_text(17)

    await check_referral(callback.from_user.id, price)

    sheet.write_answer_to_result_cell(
        callback.from_user.id,
        product.title,
        price,
        current_date
    )

    if payment.status == "succeeded":
        await callback.message.answer(text_16.text,
                                      reply_markup=await bkb.user_back_to_menu())

        await manager.done()
    else:
        await callback.answer(text_17.text,
                              show_alert=True)

