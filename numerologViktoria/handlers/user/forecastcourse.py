from aiogram import types
from keyboards.user import inline
from loader import dp
from .menu import start
from typing import Union
from .training import list_courses
from data.config import ASKEZA, VIKTORIA

WORKER_NAME = "Виктории"
WORKER_USERNAME = "viktoria_numer"

askeza_buttons = {
#     "0": {
#         "text": "О курсе",
#         "description": """
# Курс состоит из 8 подробных уроков в аудиоформате. Регулярных домашних заданий для закрепления техник.
# Также вы получаете доступ к бонусной информации «Разбор по здоровью» и «Расчет личного финансового кода».
# Всё материалы будут доступны вам в течение 6 месяцев.
# Полученные знания вы можете поменять на себе, на своих близких и также имеете возможность вступить в команду и начать зарабатывать под нашим сопровождением
# """,
#     },
#     "1": {
#         "text": "для кого курс",
#         "description": """
# - мечтаете освоить нумерологию с нуля и на практике, научится применять данные знания чтобы изменить жизнь к лучшему 

# - ощущаете сложность в общении с людьми и хотите научиться находить подход к любому человеку 

# - хотите научиться эффективно прогнозировать события. Планировать важнейшие события и подбирать правильный период  

# - хотите научиться расчитывать совместимость между людьми как в отношениях, так и в бизнесе 

# - хотите закрепить знания регулярными домашними заданиями 

# - хотите научиться расчитывать финансовый код
# """,
#     },
#     "2": {
#         "text": "программа курса",
#         "description": """
# - Вводная информация ℹ️ 

# - Прогностическая нумерология 
# вы научитесь составлять личный прогноз на любой год/месяц  + бонус 🎁 дорожная карта жизни 

# - Описание характера общее 
# - Описание характера по составным числам 

# - Разберем три основные энергии: благость, страсть, невежество. 
# большой, подробный разбор личности 

# - Исследуем, что это и зачем жить в энергии благости. 

# - Разберем предназначение, профессии, урок на воплощение, дхарма 

# - Подробное описание кармы (судьбы)

# - Изучим, почему с одним партнером мы чувствуем себя лучше, чем с другим 

# - Разберем совместимость 
# выясним как люди влияют друг на друга

# - Совместимость по энергетическому психотипу 

# - Ректификация интимной жизни по времени рождения 

# - Разберем здоровье 

# БОНУСЫ:
# - Ваши точки препятствия 
# - Научитесь расчитывать личный финансовый код
# """,
#     },
    "1": {
        "text": "стоимость и длительность",
        "description": f"""
Стоимость обучения - 12 000 ₽
Можно оплатить двумя частями.

Длительность - неделя зависит от вашего темпа. 

Реально и за пару дней все законспектировать. 

Доступ к обучению 3 месяца.
""",
    },
    "2": {
        "text": "записаться на обучение",
        "description": f"""
Чтобы задать интересующий вопрос или записаться на обучение напишите мне в личные слово «Обучение прогноз» ⬇️

@{WORKER_USERNAME} 
""",
    "whatsapp_btn": "https://api.whatsapp.com/send/?phone=79292084866&text=Привет!+Хочу+обучение+по+прогнозированию+за+12+000₽&type=phone_number&app_absent=0?"
    }
}

ASKEZA_DESCRIPTION = """
<b>Обучение</b> «Прогноз на год+прогноз на месяц+дорожная карта жизни» 

Обучение по нумерологии. 

«Прогнозирование + коррекция судьбы» 

В рамках данного обучения вы с нуля:

✔️научитесь менять негативные события на позитивные 
✔️научитесь делать прогноз на год и на месяц
✔️узнаете какая задача у вас в данном возрасте 
"""


async def list_buttons(
    callback: Union[types.CallbackQuery, types.Message], worker: str, **kwargs
):
    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(VIKTORIA), caption=ASKEZA_DESCRIPTION
            ),
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                *[
                    types.InlineKeyboardButton(
                        text=value["text"],
                        callback_data=inline.make_forecastcourse_cd(
                            level=2, worker=worker, content_type=key
                        ),
                    )
                    for key, value in askeza_buttons.items()
                ],
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=inline.make_forecastcourse_cd(level=0, worker=worker),
                ),
            ),
        )
    elif isinstance(callback, types.Message):
        await callback.answer_photo(
            photo=types.InputFile(VIKTORIA),
            caption=ASKEZA_DESCRIPTION,
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                *[
                    types.InlineKeyboardButton(
                        text=value["text"],
                        callback_data=inline.make_forecastcourse_cd(
                            level=2, worker=worker, content_type=key
                        ),
                    )
                    for key, value in askeza_buttons.items()
                ],
                types.InlineKeyboardButton(
                    text="Назад",
                    callback_data=inline.make_forecastcourse_cd(level=0, worker=worker),
                ),
            ),
        )


async def show_button(
    callback: types.CallbackQuery, worker: str, content_type: str, content_page: str
):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if askeza_buttons[content_type].get("whatsapp_btn"):
        markup.add(types.InlineKeyboardButton(text="записаться через WhatsApp", url=askeza_buttons[content_type].get("whatsapp_btn")))
    markup.add(types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_forecastcourse_cd(level=1, worker=worker),
            ))
    await callback.message.edit_caption(
        askeza_buttons[content_type]["description"],
        reply_markup=markup,
    )


@dp.callback_query_handler(inline.forecastcourse_cd.filter())
async def forecastcourse_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    worker = callback_data.get("worker")
    content_type = callback_data.get("content_type")
    content_page = callback_data.get("content_page")

    levels = {"0": list_courses, "1": list_buttons, "2": show_button}

    current_level_function = levels[level]

    await current_level_function(
        callback, worker=worker, content_type=content_type, content_page=content_page
    )
