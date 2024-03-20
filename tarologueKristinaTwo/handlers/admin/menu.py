from aiogram import types

from database import models
from keyboards.admin import inline
from loader import dp
from filters.is_admin import IsAdmin


@dp.message_handler(IsAdmin(), commands="setup")
async def setup(message: types.Message) -> None:
    service_types = [
        {"idx": 1, "name": "Консультации"},
        {"idx": 2, "name": "Ритуалы"},
    ]

    if not len(await models.ServiceType.query.gino.all()) > 0:
        for service_type in service_types:
            await models.ServiceType.create(**service_type)

    await models.Service.delete.gino.status()

    services = [
        {
            "name": "Один/два вопроса",
            "type": 1,
            "description": """
 1. Напишите:
«Хочу ответ на один/два вопроса»
 2. Сформулируйте свои вопросы
 3. Пришлите свою свежую фотографию 

💰 1 вопрос - 800₽
💰 2 вопроса - 1550₽
ПИШИ 👇🏻
@{worker}

""",
            "amount": "0",
        },
        {
            "name": "Финансы",
            "type": 1,
            "description": """
1.Ваше фин.состояние в течение года, будет ли рост в деньгах? 
2. Как пробить финансовый потолок?
3. Что мешает вашему финансовому росту? 
4. Что поможет Вам заработать в ближайшее 2-3 месяца? 
5. Деньги утекают сквозь пальцы ? 

🕐 Сроки 2-3 дня
ПИШИ 👇🏻
@{worker}

""",
            "amount": "2800",
        },
        {
            "name": "Бизнес",
            "type": 1,
            "description": """
1. Что поможет вырасти вашему делу/бизнесу? 
2. Что принесёт Вам данное дело/бизнес, если займетесь этим ?
 
🕐 Сроки 2-3 дня 
ПИШИ 👇🏻
@{worker}
""",
            "amount": "2800",
        },
        {
            "name": "работа",
            "type": 1,
            "description": """
1. Что даст Вам новая работа? 2. Работа: уходить или остаться ?
 
🕐 Сроки 2-3 дня 
ПИШИ 👇🏻
@{worker}
""",
            "amount": "2800",
        },
        {
            "name": "отношения",
            "type": 1,
            "description": """
1. Блядун или показалось? 
2. Что ждёт пару в этом году? 
3. Когда встречу того самого? Пауза или точка? Будущее этих отношений ( если недавно познакомились )? 
4. Мужчина твоей мечты ? 
5. Любовны треугольник? 
6. Планирование беременности ?
7. Расклад на выбор детского сада/школы/ университета для ребенка? 
 
🕐 Сроки 2-3 дня 
ПИШИ 👇🏻
@{worker}
""",
            "amount": "2800",
        },
        {
            "name": "Разговор с подсознанием",
            "type": 1,
            "description": """
1. Внутреннее я - разберем ваши страхи и найдем вашу реализацию 
2. Деньги - разговор о деньгах и отношении к ним с подсознанием 
 
🕐 Сроки 2-3 дня 
ПИШИ 👇🏻
@{worker}
""",
            "amount": "2800",
        },
        {
            "name": "авторские расклады",
            "type": 1,
            "description": """
1. Расклад как пройдёт отпуск? 
2. Расклад страшный/странный сон? 
3. Путь к моему желанию ? 
4. Расклад на год на все сферы жизни? 
 
🕐 Сроки 2-3 дня 
ПИШИ 👇🏻
@{worker}
""",
            "amount": "2800",
        },
        {
            "name": "Диагностика денежного канала",
            "type": 2,
            "description": """
Делаем диагностику ваших денежных каналов и потоков, смотрим что необходимо гармонизировать. Исходя из диагностики делаем практику. Практика выполняется Вами самостоятельно, носит медитативный характер, не сложна в исполнении, но очень эффективна. Я высылаю вам полную инструкцию 
🕐 Выполнение в течении суток
ПИШИ 👇🏻
@{worker}
""",
            "amount": "550",
        },
        {
            "name": "Отливка свечами «Снятие препятствий со всех жизненных дорог»",
            "type": 2,
            "description": """
Делается отливка на  свечах в течении трех дней, практика убирает все препятствия с любой сферы, гармонизирует и приводит в порядок любовь, здоровье, отношения, деньги, в зависимости от вашего запроса . 

🕐 Выполнение в течении 5 дней
ПИШИ 👇🏻
👉 @{worker}
""",
            "amount": "3000",
        },
        {
            "name": "Денежный прогноз",
            "type": 2,
            "description": """
Через какую сферу придут деньги в 2024г.?  + Заставка на телефон, старшие арканы карт Таро, для активации вашего запроса 

🕐 Выполнение в течении суток 

ПИШИ 👇🏻
@{worker}
""",
            "amount": "400",
        },
        {
            "name": "Ваше предназначение",
            "type": None,
            "description": """
Показывает вашу миссию, раскрывает ваши сильные стороны характера и показывает на какие слабости можно обратить внимание. 

🕐 Срок 2-3 дня

ПИШИ 👇🏻
@{worker}
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
