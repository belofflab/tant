from aiogram.dispatcher.filters.state import State, StatesGroup


class CUserPaymentDetail(StatesGroup):
    name = State()
    text = State()