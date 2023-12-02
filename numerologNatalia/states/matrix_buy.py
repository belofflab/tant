from aiogram.dispatcher.filters.state import State, StatesGroup


class MatrixBuy(StatesGroup):
    receipt = State()