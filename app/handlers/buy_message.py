import datetime
from operator import itemgetter

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager, StartMode, Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Column, Button, ScrollingGroup, Select, Url
from aiogram_dialog.widgets.text import Format

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb
from app.dialog.check_text import text_check, correct_text_handler, error_text_handler

from app.filters.admin_filter import AdminProtect, check_start_admin

from app.database.requests.user.add import set_user
from app.database.requests.user.update import increment_referral_count
from app.database.requests.user.select import get_user, check_referral
from app.filters.user_filter import start_user

from app.states import BuySG

from app.dialog.getters import category_getter, products_getter, product_getter, promocode_getter, payment_getter
from app.dialog.onclick import on_back, on_back_menu, on_category, on_product, on_info, on_no_promocode, \
    on_check_payment

buy = Router()

buy_dialog = Dialog(
    Window(
        Format(text="{main_text}"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="ms",
                items="categories",
                item_id_getter=itemgetter(1),
                on_click=on_category,
            ),
            width=1,
            height=5,
            id="scroll_with_pager_new",
        ),
        Column(
            Button(Format(text="{btn_text}"), id="back_to_menu", on_click=on_back_menu)
        ),
        getter=category_getter,
        state=BuySG.category,
    ),
    Window(
        Format(text="{main_text}"),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="ms",
                items="products",
                item_id_getter=itemgetter(1),
                on_click=on_product,
            ),
            width=1,
            height=5,
            id="scroll_with_pager_new",
        ),
        Column(
            Button(Format(text="{back_btn}"), id="back", on_click=on_back),
            Button(Format(text="{menu_btn}"), id="back_to_menu", on_click=on_back_menu)
        ),
        getter=products_getter,
        state=BuySG.product
    ),
    Window(
        Format(text="<b>{title}</b>\n"),
        Format(text="<b><i>{description}</i></b>\n"),
        Format(text="Стоимость: {price} руб.\n"),
        Column(
            Button(Format(text="{main_text}"), id="buy", on_click=on_info),
            Button(Format(text="{back_btn}"), id="back", on_click=on_back),
            Button(Format(text="{menu_btn}"), id="back_to_menu", on_click=on_back_menu)
        ),
        getter=product_getter,
        state=BuySG.info
    ),
    Window(
        Format(text="{main_text}"),
        TextInput(
            id='text_input_promocode',
            type_factory=text_check,
            on_success=correct_text_handler,
            on_error=error_text_handler,
        ),
        Column(
            Button(Format(text="{no_promocode_text}"), id="no_promocode", on_click=on_no_promocode),
            Button(Format(text="{back_btn}"), id="back", on_click=on_back),
            Button(Format(text="{menu_btn}"), id="back_to_menu", on_click=on_back_menu)
        ),
        getter=promocode_getter,
        state=BuySG.promocode
    ),
    Window(
        Format(text="{main_text}"),
        Column(
            Url(text=Format('{on_btn}'), url=Format('{payment_url}'), id='button_2'),
            Button(Format(text="{check_text}"), id="check", on_click=on_check_payment),
            Button(Format(text="{back_btn}"), id="back", on_click=on_back),
            Button(Format(text="{menu_btn}"), id="back_to_menu", on_click=on_back_menu)
        ),
        getter=payment_getter,
        state=BuySG.payment
    )
)


@buy.callback_query(F.data == "products")
async def products_callback(callback: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(BuySG.category, mode=StartMode.RESET_STACK)
