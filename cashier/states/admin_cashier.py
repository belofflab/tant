from aiogram.dispatcher.filters.state import State, StatesGroup


class InputAmount(StatesGroup):
    amount = State()