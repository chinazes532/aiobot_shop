import asyncio
import uuid
from yookassa import Payment

from aiogram import Bot
from aiogram_dialog import DialogManager

from app.database.requests.text.select import get_text
from app.database.requests.category.select import get_categories
from app.database.requests.product.select import get_products_by_category_id, get_product
from config import BOT_USERNAME


async def category_getter(dialog_manager: DialogManager, **kwargs):
    text_6 = await get_text(6)
    text_7 = await get_text(7)
    categories = await get_categories()

    return {
        "main_text": text_6.text,
        "btn_text": text_7.text,
        "categories": [(categories.name, categories.id) for categories in categories]
    }


async def products_getter(dialog_manager: DialogManager, **kwargs):
    text_7 = await get_text(7)
    text_8 = await get_text(8)
    text_9 = await get_text(9)
    category_id = dialog_manager.dialog_data.get("category_id")
    products = await get_products_by_category_id(int(category_id))

    return {
        "main_text": text_9.text,
        "back_btn": text_7.text,
        "menu_btn": text_8.text,
        "products": [(products.title, products.id) for products in products]
    }


async def product_getter(dialog_manager: DialogManager, **kwargs):
    product_id = dialog_manager.dialog_data.get("product_id")
    product = await get_product(int(product_id))
    text_7 = await get_text(7)
    text_8 = await get_text(8)
    text_10 = await get_text(10)

    return {
        "id": product.id,
        "title": product.title,
        "description": product.description,
        "price": product.price,
        "back_btn": text_7.text,
        "menu_btn": text_8.text,
        "main_text": text_10.text
    }


async def promocode_getter(dialog_manager: DialogManager, **kwargs):
    text_11 = await get_text(11)
    text_12 = await get_text(12)
    text_7 = await get_text(7)
    text_8 = await get_text(8)

    return {
        "main_text": text_11.text,
        "no_promocode_text": text_12.text,
        "back_btn": text_7.text,
        "menu_btn": text_8.text
    }


async def payment_getter(dialog_manager: DialogManager, bot: Bot, **kwargs):
    product_id = dialog_manager.dialog_data.get("product_id")
    price = dialog_manager.dialog_data.get("price")
    product = await get_product(int(product_id))
    text_13 = await get_text(13)
    text_14 = await get_text(14)
    text_15 = await get_text(15)
    text_7 = await get_text(7)
    text_8 = await get_text(8)

    payment = Payment.create({
        "amount": {
            "value": f'{price}',
            "currency": 'RUB'
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/{BOT_USERNAME}"
        },
        "capture": True,
        "description": f"{product.title}",
    }, uuid.uuid4())

    dialog_manager.dialog_data.update(payment_id=payment.id)

    return {
        "payment_url": payment.confirmation.confirmation_url,
        "payment_id": payment.id,
        "main_text": text_13.text,
        "back_btn": text_7.text,
        "menu_btn": text_8.text,
        "on_btn": text_14.text,
        "check_text": text_15.text
    }


