from aiogram.dispatcher.filters.state import State, StatesGroup


class DebitState(StatesGroup):
    amount = State()