from aiogram.dispatcher.filters.state import State, StatesGroup


class RewardState(StatesGroup):
    amount = State()