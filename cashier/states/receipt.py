from aiogram.dispatcher.filters.state import State, StatesGroup


class ReceiptState(StatesGroup):
    receipt = State()