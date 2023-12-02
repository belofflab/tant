import requests
from typing import Union

from aiogram import types
from data.config import VALERIA, SERVER_URL
from database import models
from keyboards.user import inline
from aiogram.dispatcher import FSMContext
from filters.is_connected import IsConnected
from loader import dp

MENU_CAPTION = """
Всем привет 👋 
Меня зовут Полина , я таролог🧙‍♀️

Мой путь начался еще с 2020 , начиналось все с обычных раскладов подружкам , но на этом я не остановилась и продолжила погружаться в тему эзотерики✨

Сейчас я уже помогаю людям ответить на любой вопрос в разных сферах. У меня свой индивидуальный подход к каждому клиенту.Не стоит стесняться, со мной вы можете обсудить любую тему , которая вас тревожит🥰
"""

async def get_or_create_user(user_id: int, username: str) -> models.User:
    user = await models.User.query.where(models.User.idx == user_id).gino.first()
    if user is not None:
        return user
    return await models.User.create(
        idx=user_id, username=username if username is not None else "no username"
    )

@dp.message_handler(commands="start")
async def start(message: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    if isinstance(message, types.Message):
        account = message.get_args()
        if account not in ["polina_tarolog", ]:
            account = "polina_tarolog"

        await get_or_create_user(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
        requests.post(
            url=SERVER_URL + f"/users/?worker_name={account}",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "id": message.from_user.id,
                "username": message.from_user.username,
                "first_name": "FROM",
                "last_name": "BOT",
                "worker": 99,
            },
        )
        await message.answer_photo(
            photo=types.InputFile(VALERIA),
            caption=MENU_CAPTION,
            reply_markup=await inline.menu_keyboard(worker=account),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        await message.message.edit_media(
            media = types.InputMediaPhoto(
                media=types.InputFile(VALERIA),
                caption=MENU_CAPTION
            ), reply_markup=await inline.menu_keyboard(worker=kwargs.get("worker"))
        )


async def list_service_types(callback: types.CallbackQuery, worker, **kwargs) -> None:
    markup = await inline.service_types_keyboard(worker=worker)
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"
    await callback.message.edit_caption(caption=text, reply_markup=markup)


async def list_services(
    callback: types.CallbackQuery, service_type: str, worker: str, **kwargs
) -> None:
    markup = await inline.services_keyboard(service_type, worker)
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"
    await callback.message.edit_caption(caption=text, reply_markup=markup)


async def show_service(
    callback: types.CallbackQuery, service_type: str, service: str, worker: str
) -> None:
    markup = await inline.show_service(service=service, service_type=service_type, worker=worker)
    q_service = await models.Service.query.where(
        models.Service.idx == int(service)
    ).gino.first()

    await callback.message.edit_caption(
        caption=f"""
{q_service.description.format(worker=worker)}
{f"Стоимость: <i>{int(q_service.amount)}₽</i> " if  q_service.amount > 0 else ''}
""",
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("free"))
async def free(callback: types.CallbackQuery) -> None:
    worker = callback.data.split("#")[-1]
    requests.post(
            url=SERVER_URL + "/users/free/",
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
    await callback.message.edit_caption(
        caption=f"""
✏️Сформулируйте пожалуйста свой вопрос и направьте свое фото/имя, если он связан с вами, если в раскладе будут присутствовать и другие люди, то тоже нужно их фото/имя)

Всё это направьте в личные сообщения тарологу Полине 👇🏻

@{worker}
""",
        reply_markup=await inline.free_markup(worker=worker),
    )


@dp.callback_query_handler(inline.service_cd.filter())
async def service_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    service_type = callback_data.get("type")
    service = callback_data.get("service")
    worker = callback_data.get("worker")

    levels = {
        "0": start,
        # "1": list_service_types,
        "1": list_services,
        "2": show_service,
    }

    current_level_function = levels[level]

    await current_level_function(
        callback, service=service, service_type=service_type, worker=worker
    )
