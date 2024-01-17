from aiogram.dispatcher.filters.state import State, StatesGroup


class TrainingBuy(StatesGroup):
    receipt = State()