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

    if not len(await models.ServiceType.query.gino.all()) > 0:
        for service_type in service_types:
            await models.ServiceType.create(**service_type)

    await models.Service.delete()

    services = [
        {
            "name": "Прогноз на 2024 год",
            "type": 1,
            "description": """
Чтобы мечты сбывались, нужно потрудиться и быть готовым к её исполнению внутренне! 
Годовой прогноз - это ваша карта, с которой вы будете идти от месяца к месяцу, выполняя определенные действия, которые в дальнейшем приведут вас к цели, к себе настоящим, к успеху, к жизни здесь и сейчас.
Всем здоровья, радости, благополучия, любви и конечно же найти свой путь!
После моего прогноза ваша жизнь разделится на До и После. Проверим ? 

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
