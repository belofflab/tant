import requests
import asyncio
from typing import Union

from aiogram import types
from data.config import WORKER_PHOTO, SERVER_URL, WORKER_USERNAME
from database import models
from keyboards.user import inline
from loader import dp

MENU_CAPTION = """
Здравствуйте 😊
Меня зовут Кристина. Я практикующий нумеролог и консультант по матрице судьбы💫
 
Консультация со мной поможет вам лучше узнать себя, свой потенциал и способности, определить путь дальнейшего развития, чтобы улучшить карму рода. Я помогу определиться с выбором профессии и идеального партнёра, а благодаря прогнозу, вы точно будете знать - стоит ли покупать машину (квартиру) и запускать своё собственное дело.
Уверена, что каждый найдёт то, что ему нужно! 

Я делаю расчёт взрослой, детской матрицы судьбы, совместимость партнёров, также составляю прогноз на год.

Жду Вас на консультации♥️
"""

async def get_or_create_user(user_id: int, username: str) -> models.User:
    user = await models.User.query.where(models.User.idx == user_id).gino.first()
    if user is not None:
        return user
    return await models.User.create(
        idx=user_id, username=username if username is not None else "no username"
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
                "worker": 999999, # WORKER ID 
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
                "worker": 999999,
            },
        )

@dp.message_handler(commands="start")
async def start(message: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    if isinstance(message, types.Message):
        account = message.get_args()
        if account not in [WORKER_USERNAME, ]:
            account = WORKER_USERNAME

        await get_or_create_user(
            user_id=message.from_user.id,
            username=message.from_user.username
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

@dp.callback_query_handler( lambda c: c.data.startswith("free"))
async def free(callback: types.CallbackQuery) -> None:
    worker = callback.data.split("#")[-1]
    asyncio.get_event_loop().create_task(update_user_touch(callback=callback))
    await callback.message.edit_caption(
        caption=f"""
Отправьте дату своего рождения мне в личном сообщении 
<b>НАЖАТЬ</b> 👉🏻  @{worker}

Пример: 12.09.1978
""",
        reply_markup=await inline.free_markup(worker=worker),
    )