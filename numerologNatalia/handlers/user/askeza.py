from aiogram import types
from keyboards.user import inline
from loader import dp
from .menu import start
from typing import Union
from data.config import ASKEZA

WORKER_NAME = "Наталье"
WORKER_USERNAME = "Natali_numerologist"

askeza_buttons = {
    "0": {
        "text": "Как это работает?",
        "description": """
✅Определяем намерение. На что именно берем аскезу. У всех она своя. 

✅Подготовка (правильное очищение) 

✅Определяем намерение. Ради какой цели/желания держим аскезу (все это также индивидуально)

✅Пишем заявление. Правильная формулировка. Каждое заявление проверяется и корректируется при необходимости.

✅Изучаем правила прохождения аскезы 

✅Уже во время прохождения аскезы вы начнете получать приятные бонусы, что подтвердит, что вы на верном пути

✅Учимся правильно принимать и благодарить 

✅На протяжении аскезы вы также выполняете практики и ритуалы которые дают эксперты которые также приближают вас к исполнению желания 

✅Правильный выход из аскезы
""",
    },
    "1": {
        "text": "Примеры аскез",
        "description": """
Здесь представлены самые популярные примеры аскез.

❌Отказ от алкоголя 
❌Отказ от курения 
❌Отказ от матерных слов
❌Отказ от кофеина 
❌Отказ от сахара
❌Отказ от мучного 
❌Отказ от молочных продуктов 

✅ 10 000 шагов в день 
✅ мыть посуду на ночь 
✅Физические упражнения 
✅Ранний подъем  (соблюдать режим)
✅Чтение книг
✅Выучить билеты ПДД
✅Пройти обучение 
✅Обращать внимание только на положительное 
✅Любовь к себе, а не самоистязание
""",
    },
    "2": {
        "text": "Для кого подойдет",
        "description": """
🪄 Кто долгое время не может взять себя в руки 

🪄 Зависит от вредных привычек 

🪄 Кто хочет выработать самодисциплину 

🪄 Пройти обучение вовремя 

🪄 Привести свое тело и кожу в порядок 

🪄 Сделать первый шаг на встречу своим целям и желаниям 

🪄 Научиться принципам аскезы

🪄 Получить мощный заряд для движения вперед
""",
    },
    "3": {
        "text": "Задать вопрос",
        "description": f"""
Если вы все ещё не можете понять нужна ли вам аскеза, не можете определиться на что брать аскезу или какое желание/цель вы хотите исполнить Пишите в личные сообщения {WORKER_NAME} 
👇🏻

@{WORKER_USERNAME}

«Аскеза. Вопрос» (задайте свой вопрос)
""",
    },
    "4": {
        "text": "Стоимость/длительность",
        "description": """
Стоимость участия.
Для тех кто вступил 

До нового года - 500₽
После Нового года - 800₽

Длительность - 21 день (с 12.01 - по 01.02)
""",
    },
    "5": {
        "text": "Принять участие",
        "description": f"""
Если вы готовы принять участие в групповой аскезе с сопровождением напишите в Личные сообщения {WORKER_NAME} 
👇🏻

@{WORKER_USERNAME}

«Хочу участвовать в аскезе»
""",
    },
}

ASKEZA_DESCRIPTION = """
После того как ты внедришь аскезу в свою жизнь ты станешь человеком-магнитом который который притягивает в свою жизнь все блага мира. 🧚🏻‍♀️ 

<b>Этот метод работает.</b>

- Наша команда регулярно практикует аскезу с 2021 года. 

- Более 350 участников прошли аскезу и проходят повторно.

<b>Как исполняется желание с помощью аскезы 👇🏻</b>

Приведу пример:

У вас была зависимость от курения. 
Вы берете аскезу на отказ. 
У вас освобождается большое количество энергии которая высвободится в процессе взятой аскезы и вся эта энергия пойдет на исполнение вашего желания которое вы укажете в заявлении.

Важно брать аскезу которая вам сложно дается так как именно там огромный ресурс который вы направите в нужное русло. 

А как это делать мы научим 🫶🏻
"""


async def list_buttons(
    callback: Union[types.CallbackQuery, types.Message], worker: str, **kwargs
):
    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(ASKEZA), caption=ASKEZA_DESCRIPTION
            ),
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                *[
                    types.InlineKeyboardButton(
                        text=value["text"],
                        callback_data=inline.make_askeza_cd(
                            level=2, worker=worker, content_type=key
                        ),
                    )
                    for key, value in askeza_buttons.items()
                ],
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=inline.make_askeza_cd(level=0, worker=worker),
                ),
            ),
        )
    elif isinstance(callback, types.Message):
        await callback.answer_photo(
            photo=types.InputFile(ASKEZA),
            caption=ASKEZA_DESCRIPTION,
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                *[
                    types.InlineKeyboardButton(
                        text=value["text"],
                        callback_data=inline.make_askeza_cd(
                            level=2, worker=worker, content_type=key
                        ),
                    )
                    for key, value in askeza_buttons.items()
                ],
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=inline.make_askeza_cd(level=0, worker=worker),
                ),
            ),
        )


async def show_button(
    callback: types.CallbackQuery, worker: str, content_type: str, content_page: str
):
    await callback.message.edit_caption(
        askeza_buttons[content_type]["description"],
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_askeza_cd(level=1, worker=worker),
            )
        ),
    )


@dp.callback_query_handler(inline.askeza_cd.filter())
async def askeza_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    worker = callback_data.get("worker")
    content_type = callback_data.get("content_type")
    content_page = callback_data.get("content_page")

    levels = {"0": start, "1": list_buttons, "2": show_button}

    current_level_function = levels[level]

    await current_level_function(
        callback, worker=worker, content_type=content_type, content_page=content_page
    )
