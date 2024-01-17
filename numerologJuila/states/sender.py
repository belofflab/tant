from aiogram.dispatcher.filters.state import State, StatesGroup


class Sender(StatesGroup):
    photo = State()
    text = State()
    buttons = State()
    users = State()