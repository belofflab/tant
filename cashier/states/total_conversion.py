from aiogram.dispatcher.filters.state import State, StatesGroup


class TotalConversionState(StatesGroup):
    date_range = State()