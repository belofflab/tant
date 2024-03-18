from aiogram import types
from loader import dp
from .menu import start

WORKER_NAME = "Виктории"
WORKER_USERNAME = "viktoria_numer"


TEAM_DESCRIPTION = f"""
Если вы являетесь экспертом в сфере нумерологии/астрологии/таро и других подобных направлений, не знаете, как себя продвигать, как на этом зарабатывать, - мы вас научим. 

Если вы только новичок, и определяетесь с нишей, можем обговорить условия.

Вложения не требуются. Только работа под нашим руководством. 

Вы можете выйти на любой доход, все зависит от того, как активно вы будете работать и сколько времени уделять.

По всем вопросам писать {WORKER_NAME} 👇🏻

@{WORKER_USERNAME}

Напишите «Хочу в команду»
"""


@dp.callback_query_handler(lambda c: c.data.startswith("wanttoteam"))
async def wanttoteam(callback: types.CallbackQuery):
    worker = callback.data.split("#")[-1]
    await callback.message.edit_caption(
        caption=TEAM_DESCRIPTION,
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Назад", callback_data=f"backwanttoteam#{worker}"
            )
        ),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("backwanttoteam"))
async def backwanttoteam(callback: types.CallbackQuery):
    worker = callback.data.split("#")[-1]
    await start(message=callback, worker=worker)
