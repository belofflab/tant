from aiogram.dispatcher.filters.state import State, StatesGroup


class Signup(StatesGroup):
    full_name = State()
    mobile_phone = State()
    email = State()