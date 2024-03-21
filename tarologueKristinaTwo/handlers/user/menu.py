import requests
import asyncio
import datetime
from typing import Union

from aiogram import types
from data.config import WORKER_PHOTO, SERVER_URL, WORKER_USERNAME
from database import models
from keyboards.user import inline
from loader import dp

MENU_CAPTION = """
Приветствую тебя мой милый друг! Рада тебе ❤️

Меня зовут Кристина. Я сертифицированый таролог. Отвечу на любой волнующий вопрос и сниму тревоги. Расставим вместе все точки над “I”. Чтобы нам стать ближе, жми кнопку бесплатная  консультация, увидимся 💗
"""

# async def save_user(message: types.Message):
#     requests.post(
#         url=SERVER_URL + f"/users/",
#         headers={
#             "accept": "application/json",
#             "Content-Type": "application/json",
#         },
#         json={
#             "id": message.from_user.id,
#             "username": message.from_user.username,
#             "first_name": message.from_user.full_name,
#             "worker_bot": BOT_UUID,
#         },
#     )


# async def update_user_touch(callback: types.CallbackQuery):
#     requests.post(
#         url=SERVER_URL + "/users/free/",
#         headers={
#             "accept": "application/json",
#             "Content-Type": "application/json",
#         },
#         json={
#             "id": callback.from_user.id,
#             "username": callback.from_user.username,
#             "first_name": callback.from_user.full_name,
#             "worker_bot": BOT_UUID,
#         },
#     )


async def get_or_create_user(user_id: int, username: str, full_name: str) -> models.User:
    user = await models.User.query.where(models.User.idx == user_id).gino.first()
    if user is not None:
        to_update = {"is_active": True, "last_active": datetime.datetime.now()}
        if user.full_name != full_name or user.username != username:
            to_update["full_name"] = full_name
            to_update["username"] = username
        await models.User.update.values(**to_update).where(
                models.User.idx == user.idx
            ).gino.status()
        return user
    return await models.User.create(
        idx=user_id, username=username, full_name=full_name
    )

async def proceed_signin(message, worker_name):
    await get_or_create_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
    requests.post(
        url=SERVER_URL + f"/users/?worker_name={worker_name}",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "worker": 567890, # WORKER ID 
        },
    )
async def save_user(worker_name: str, message: types.Message):
    requests.post(
            url=SERVER_URL + f"/users/?worker_name={worker_name}",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "id": message.from_user.id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "worker": 567890, # WORKER ID 
            },
        )
    
async def update_user_touch(callback: types.CallbackQuery):
    requests.post(
            url=SERVER_URL + "/users/free/",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "id": callback.from_user.id,
                "username": callback.from_user.username,
                "first_name": callback.from_user.first_name,
                "last_name": callback.from_user.last_name,
                "worker": 567890,
            },
        )

@dp.message_handler(commands="start")
async def start(message: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    if isinstance(message, types.Message):
        from . import askeza
        account = message.get_args()
        if account == "askeza":
            await proceed_signin(message=message, worker_name=WORKER_USERNAME)
            return await askeza.list_buttons(callback=message, worker=WORKER_USERNAME)
        if account == "services":
            from .services import list_service_types
            await proceed_signin(message=message, worker_name=WORKER_USERNAME)
            return await list_service_types(callback=message,  worker=WORKER_USERNAME)
        if account == "taro":
            from .training import list_courses
            await proceed_signin(message=message, worker_name=WORKER_USERNAME)
            return await list_courses(callback=message, worker=WORKER_USERNAME)
        if account == "free":
            await proceed_signin(message=message, worker_name=WORKER_USERNAME)
            return await free(callback=message, worker=WORKER_USERNAME)
        if account not in [WORKER_USERNAME, ]:
            account = WORKER_USERNAME

        await get_or_create_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        asyncio.get_event_loop().create_task(save_user(worker_name=WORKER_USERNAME, message=message))
        await message.answer_photo(
            photo=types.InputFile(WORKER_PHOTO),
            caption=MENU_CAPTION,
            reply_markup=await inline.menu_keyboard(worker=account),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        await message.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(WORKER_PHOTO),
                caption=MENU_CAPTION
            ),
            reply_markup=await inline.menu_keyboard(worker=kwargs.get("worker"))
        )

@dp.callback_query_handler(lambda c: c.data.startswith("free"))
async def free(callback: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    asyncio.get_event_loop().create_task(update_user_touch(callback=callback))
    if isinstance(callback, types.Message):
        worker = kwargs.get("worker")
        await callback.answer_photo(
        photo=types.InputFile(WORKER_PHOTO),
        caption=f"""
Отправьте дату своего рождения мне в личном сообщении 
<b>НАЖАТЬ</b> 👉🏻  @{worker}

Пример: 12.09.1978
""",
        reply_markup=await inline.free_markup(worker=worker),
    )
    elif isinstance(callback, types.CallbackQuery):
        worker = callback.data.split("#")[-1]
        await callback.message.edit_caption(
            caption=f"""
Отправьте дату своего рождения мне в личном сообщении 
<b>НАЖАТЬ</b> 👉🏻  @{worker}

Пример: 12.09.1978
""",
            reply_markup=await inline.free_markup(worker=worker),
        )