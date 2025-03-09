import datetime

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput

from app.database.requests.product.select import get_product
from app.database.requests.promocode.select import get_promocode_by_name
from app.database.requests.promocode.update import update_promocode_count

from app.states import BuySG


def text_check(text: str) -> str:
    if len(text) < 3 or len(text) > 2200:
        raise ValueError
    return text


async def correct_text_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str) -> None:
    name = message.text
    promocode = await get_promocode_by_name(name)
    current_time = datetime.datetime.now().strftime("%d.%m.%Y")

    if promocode:
        if promocode.count > 0:
            if not promocode.end_date:
                dialog_manager.dialog_data.update(
                    promocode_id=promocode.id
                )
                product_id = dialog_manager.dialog_data.get("product_id")
                product = await get_product(int(product_id))

                price = product.price * (1 - promocode.percent / 100)

                dialog_manager.dialog_data.update(
                    price=price
                )

                await update_promocode_count(promocode.id)

                await message.answer(f"<b>Промокод успешно применен!</b>\n"
                                     f"<b>Итоговая цена составляет:</b> <s>{product.price}</s> <i>{price:.2f}</i>")

                await dialog_manager.next()
            elif promocode.end_date < current_time:
                await dialog_manager.switch_to(BuySG.promocode)
        else:
            await dialog_manager.switch_to(BuySG.promocode)
    else:
        await dialog_manager.switch_to(BuySG.promocode)



async def error_text_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError):
    await message.answer(
        text='Вы ввели некорректный текст. Попробуйте еще раз'
    )