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
Привет 👋. Меня зовут Валерия, твой персональный Таролог) Практикую гадание с 2020 года.
Мое знакомство с магией произошло еще в детстве, я случайно наткнулась на книги своей прабабушки и с этого началась моя история изучения таро. Знания по таро в моей семье собирались и передавались из поколения в поколение🧙

🌞 Опыт и сила моих предков помогает мне оказывать качественную работу над вашими вопросами. А энергия которую я чувствую от высших сил, помогает с легкостью разобрать самый сложный вопрос, на который никто другой не сможет ответить

💥 Что я предлагаю
Моя задача как профессионала, разобрать вашу ситуацию по полочкам, а главное помочь!
Я хочу, что бы Вы нашли своего проводника, который будет помогать вам всю жизнь и приведет вас к вершине своего познания.
Ты находишься именно там где должен был оказаться 🙏
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
        if account not in ["tarolog_va1eria", ]:
            account = "tarolog_va1eria"

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
                "worker": 999999,
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
            media=types.InputMediaPhoto(
                media=types.InputFile(VALERIA),
                caption=MENU_CAPTION
            ),
            reply_markup=await inline.menu_keyboard(worker=kwargs.get("worker"))
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


@dp.callback_query_handler( lambda c: c.data.startswith("free"))
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

Всё это направьте в личные сообщения тарологу Лере 👇🏻

@{worker}
""",
        reply_markup=await inline.free_markup(worker=worker),
    )


@dp.callback_query_handler( inline.service_cd.filter())
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
