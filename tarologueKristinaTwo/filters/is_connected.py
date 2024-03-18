import requests

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery
from database import models
from data.config import SERVER_URL


async def get_or_create_user(user_id: int, username: str) -> models.User:
    user = await models.User.query.where(models.User.idx == user_id).gino.first()
    if user is not None:
        return user
    return await models.User.create(
        idx=user_id, username=username if username is not None else "no username"
    )

class IsConnected(BoundFilter):
    async def check(_, callback: CallbackQuery):
        await get_or_create_user(callback.from_user.id, callback.from_user.username)
        requests.post(
            url=SERVER_URL + "/users/?worker_name=",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "id": callback.from_user.id,
                "username": callback.from_user.username,
                "first_name": "FROM",
                "last_name": "BOT",
                "worker": 999,
            },
        )
        return True
