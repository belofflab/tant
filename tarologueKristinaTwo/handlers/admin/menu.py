from aiogram import types

from database import models
from keyboards.admin import inline
from loader import dp
from filters.is_admin import IsAdmin


@dp.message_handler(IsAdmin(), commands="setup")
async def setup(message: types.Message) -> None:
    service_types = [
        {"idx": 1, "name": "Мои услуги"},
        {"idx": 2, "name": "Ритуалы"},
    ]

    if not len(await models.ServiceType.query.gino.all()) > 0:
        for service_type in service_types:
            await models.ServiceType.create(**service_type)

    await models.Service.delete.gino.status()

    services = [
        {
            "name": "Один вопрос 🌷",
            "type": 1,
            "description": """
1. Напишите:
«Хочу ответ на один вопрос
2. Сформулируйте свой вопрос 
3. Пришлите свою свежую фотографию 
4. Все это пришлите мне👉 @{worker}

""",
            "amount": "800",
        },
        {
            "name": "Два вопроса 🌷",
            "type": 1,
            "description": """
 1. Напишите:
«Хочу ответ на два вопроса
 2. Сформулируйте свои вопросы
 3. Пришлите свою свежую фотографию 
 4. Все это пришлите мне 👉 @{worker}

""",
            "amount": "1550",
        },
        {
            "name": "Полный разбор вашей ситуации по определенной теме 🌷",
            "type": 1,
            "description": """
тут исправить
👉 @{worker}
""",
            "amount": "2800",
        },
        {
            "name": "Диагностика денежного канала",
            "type": 2,
            "description": """
Диагностика денежного канала + практика на увеличение финансовых возможностей. Ритуал выполняется вами самостоятельно. Я даю полную, подробную инструкцию. 
👉 @{worker}
""",
            "amount": "550",
        },
        {
            "name": "Снятие приветствий со всех жизненных дорог",
            "type": 2,
            "description": """
Отливка свечами «Снятие приветствий со всех жизненных дорог»( отношения, деньги, бизнес)
👉 @{worker}
""",
            "amount": "2000",
        },
        {
            "name": "Денежный прогноз",
            "type": 2,
            "description": """
Денежный прогноз, через какую сферу придут деньги в 2024г. + заставка на телефон, старшие арканы карт Таро, для активации вашего запроса 
👉 @{worker}
""",
            "amount": "400",
        },
    ]

    for service in services:
        await models.Service.create(**service)

    await message.answer("ok")


@dp.message_handler(IsAdmin(), commands="admin")
async def admin_menu(message: types.Message) -> None:
    markup = await inline.menu_keyboard()
    users = await models.User.query.gino.all()
    await message.answer(
        f"""
Доступное меню: 
Сейчас пользователей: {len(users)}
""",
        reply_markup=markup,
    )


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "admin_menu")
async def admin_menu_c(callback: types.CallbackQuery) -> None:
    markup = await inline.menu_keyboard()

    await callback.message.edit_reply_markup(reply_markup=markup)
