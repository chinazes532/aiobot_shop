from aiogram.fsm.state import State, StatesGroup


class BuySG(StatesGroup):
    category = State()
    product = State()
    info = State()
    promocode = State()
    payment = State()