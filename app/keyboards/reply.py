from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Админ-панель', web_app=WebAppInfo(url='https://your-web-app-url.com'))
        ]
    ],
    resize_keyboard=True
)