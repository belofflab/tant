from aiogram.dispatcher.filters.state import State, StatesGroup


class UserPaymentDetail(StatesGroup):
    name = State()
    text = State()