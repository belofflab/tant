from aiogram.dispatcher.filters.state import State, StatesGroup


class RefillState(StatesGroup):
    amount = State()