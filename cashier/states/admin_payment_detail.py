from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminPaymentDetail(StatesGroup):
    name = State()
    text = State()