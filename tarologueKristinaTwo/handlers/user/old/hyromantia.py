from aiogram import types
from keyboards.user import inline
from loader import dp
from ..menu import start

WORKER_NAME = "Валерии"
WORKER_USERNAME = "tarolog_va1eria"

hyromantia_buttons = {
    "0": {
        "text": "Детский 👧🏻👦🏼🧒🏽",
        "description": """
1 кнопка

Детский 👧🏻👦🏼🧒🏽

Детский разбор я делаю для детей от 1 года и до 14 лет, что он включает в себя:
 • <b>Общие положения</b> (каким вырастет ребенок, какие черты его характера проявлены больше всего)
 • <b>Планеты в «+»</b> (какие планеты влияют на ребенка положительно)
 • <b>Планеты в «-»</b> (какие планеты влияют отрицательно на его характер)
 • <b>Профессиональное ориентирование</b> (в каких сферах стоит реализовывать ребенка, в каких сферах он не сможет работать)
 • <b>Карма прошлой жизни</b> (какой кармический долг ему следует вернуть, с какими трудностями столкнется в этой жизни, с чем ему стоит помочь)
+ 1 вопрос
Пример: Когда станет самостоятельным?
Почему у него проблемы в учебе?
и другие. За каждый последующий вопрос доплата 150 рублей 

Стоимость детского разбора: <b>999</b> рублей.

Пиши мне в личные сообщения «Детские ладони» 👇🏼

@{worker}
"""
    },
    "1": {
        "text": "Взрослый 👨🏻‍🦱👩🏼",
        "description": """
Взрослый разбор я делаю с 14 лет. Он включает в себя:
 • <b>Общие положения</b> (как вас видят окружающие, то как вы себя ощущаете, ваши скрытые черты характера. Что стоит открывать в себе, а что лучше не показывать)
 • <b>Планеты в «+»</b> (какие планеты влияют на вас положительно)
 • <b>Планеты в «-»</b> (какие планеты влияют на вас отрицательно)
 • <b>Профессиональное ориентирование</b> (в какой профессии вы точно приуспеете)
 • <b>Карма прошлой жизни</b> (что вам следует проработать, чтобы убрать «хвосты» прошлой жизни, что следует укрепить в себе, чтобы добиться успеха прошлой жизни)
 • <b>Карма этой жизни</b> (как испортилась карма этой жизни)
 • <b>Ваши теневые стороны</b> (то от чего вы зависите, ваши грехи и секреты)
+ 2 вопроса
Пример:
Когда разбогатею?
Когда в мою жизнь прийдет «тот самый» ?
и другие. За каждый последующий вопрос 150 рублей. Вопрос может быть как на короткий срок, так и на продолжительный.
Стоимость взрослого разбора: <b>1499</b> рублей.

Пиши в личные сообщения «Взрослые ладони» 👇🏼
@{worker}
""",
    },
    "2": {
        "text": "Мини разбор 👨‍👩‍👦",
        "description": """
Этот разбор не зависит от возраста. В него входит 
 • <b>Общие положения</b> (как вас видят окружающие, то как вы себя ощущаете, ваши скрытые черты характера. Что стоит открывать в себе, а что лучше не показывать)
 • <b>Планеты в «+»</b> (какие планеты влияют на вас положительно)
 • <b>Планеты в «-»</b> (какие планеты влияют на вас отрицательно)

Если возникают какие-либо вопросы 
Пример:
Стоит ли менять работу?
Стоимость 150 рублей. И так же все последующие.

Стоимость мини разбора <b>499</b>. рублей.
Если после этого хотите получить полный разбор, его стоимость 1000 рублей.

Пиши в личные «Мини ладони» 👇🏼
@{worker}
""",
    },
}

HYROMANTIA_DESCRIPTION = """
Хиромантия 

Ваши ладони, вы когда нибудь интересовались ими???
А что если я скажу, что ладони вторые глаза человека. Что на них точно так же отражается ваша душа.
А если я вам расскажу даже больше, чем вы сами знаете о себе.

А что же можно узнать? 🤔 <b>ВСЕ!</b>
Когда у вас родится ребенок - <b>легко</b>
Когда замуж - <b>элементарно</b>
Когда бизнес попрет в гору - <b>проще простого</b>

Хочешь получить ответы на любой из этих вопросов или на большое количество каких-либо других?

Хочешь узнать как направить своего ребенка и узнать какой он на самом деле?

👇🏼👇🏼👇🏼 <b>выбирай кнопку по душе </b>👇🏼👇🏼👇🏼
"""


async def list_buttons(callback: types.CallbackQuery, worker: str, **kwargs):
    await callback.message.edit_caption(
        caption=HYROMANTIA_DESCRIPTION,
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            *[
                types.InlineKeyboardButton(
                    text=value["text"],
                    callback_data=inline.make_hyromantia_cd(
                        level=2, worker=worker, content_type=key
                    ),
                )
                for key, value in hyromantia_buttons.items()
            ],
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_hyromantia_cd(level=0, worker=worker),
            ),
        ),
    )


async def show_button(
    callback: types.CallbackQuery, worker: str, content_type: str, content_page: str
):
    await callback.message.edit_caption(
        hyromantia_buttons[content_type]["description"].format(worker=worker),
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_hyromantia_cd(level=1, worker=worker),
            )
        ),
    )


@dp.callback_query_handler(inline.hyromantia_cd.filter())
async def hyromantia_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    worker = callback_data.get("worker")
    content_type = callback_data.get("content_type")
    content_page = callback_data.get("content_page")

    levels = {"0": start, "1": list_buttons, "2": show_button}

    current_level_function = levels[level]

    await current_level_function(
        callback, worker=worker, content_type=content_type, content_page=content_page
    )
