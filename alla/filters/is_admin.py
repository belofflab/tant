from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery
from loader import WDATA


class IsAdmin(BoundFilter):
    async def check(_, callback: CallbackQuery):
        if callback.from_user.id in [worker["user"]["id"] for worker in WDATA["workers"]]:
            return True
        return False
