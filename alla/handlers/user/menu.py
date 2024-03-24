from typing import Union

from aiogram import types
from data.config import WORKER_PHOTO
from database import models
from keyboards.user import inline
from loader import dp, analytics

from loader import WORKER_USERNAME, WDATA

@dp.message_handler(commands="start")
async def start(message: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    analytics.send_request("/users/", json={
                "id": message.from_user.id,
                "username": message.from_user.username,
                "full_name": message.from_user.full_name,
                "worker_bot": WDATA["bot"]["uid"], 
            })
    if isinstance(message, types.Message):
        from . import askeza
        account = message.get_args()
        if account == "askeza":
            return await askeza.list_buttons(callback=message, worker=WORKER_USERNAME)
        if account == "services":
            from .services import list_service_types
            return await list_service_types(callback=message,  worker=WORKER_USERNAME)
        if account == "taro":
            from .training import list_courses
            return await list_courses(callback=message, worker=WORKER_USERNAME)
        if account == "free":
            return await free(callback=message, worker=WORKER_USERNAME)
        if account not in [WORKER_USERNAME, ]:
            account = WORKER_USERNAME

        await message.answer_photo(
            photo=types.InputFile(WORKER_PHOTO),
            caption=WDATA["bot"]["main_description"],
            reply_markup=await inline.menu_keyboard(worker=account),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        await message.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(WORKER_PHOTO),
                caption=WDATA["bot"]["main_description"]
            ),
            reply_markup=await inline.menu_keyboard(worker=kwargs.get("worker"))
        )

@dp.callback_query_handler(lambda c: c.data.startswith("free"))
async def free(callback: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
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