from aiogram import types

from database import models
from keyboards.admin import inline
from loader import dp
from filters.is_admin import IsAdmin


@dp.message_handler(IsAdmin(), commands="setup")
async def setup(message: types.Message) -> None:
    service_types = [
        {"idx": 1, "name": "test"},
    ]

    for service_type in service_types:
        await models.ServiceType.create(**service_type)

    services = [
        {
            "name": "Прогноз на 2024 год",
            "type": 1,
            "description": """
То, что вы называете удачей — это по сути правильные действия в правильное время. 
Данный прогноз является инструкцией и вашим персональным объёмом работы на этот год.
Для всего есть своё благоприятное время, покупка машины, запуск бизнеса, инвестиции, недвижимость. 
Если вы выбрали неблагоприятное время, все будет против вас.
🙎‍♀️@{worker}

""",
            "amount": "2024",
        }
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
