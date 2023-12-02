import requests
import datetime
from aiogram import types
from loader import dp
from data.config import SERVER_URL


@dp.message_handler(commands=["rate", "rates", "рейтинг"])
async def rates(message: types.Message):
    workers_rates = requests.get(SERVER_URL + f"/workers/rates/")
    if workers_rates.status_code != 200:
        return await message.answer(
            "Ошибка сервера! Свяжитесь с тех.поддержкой @belofflab"
        )
    workers_rates_data = workers_rates.json()
    sorted_data = dict(
        sorted(workers_rates_data.items(), key=lambda item: item[1], reverse=True)
    )
    await message.answer(
        "🌟<b>Рейтинг за весь период:</b>🌟\n\n"
        + "\n".join(
            [
                f"💫 {name} {amount}₽"
                    if idx + 1 <= 1
                    else
                    f"{idx + 1}. {name} {amount}₽"
                for idx, (name, amount) in enumerate(sorted_data.items())
            ]
        ),
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="За текущий месяц", callback_data="wrates#month"
            )
        ),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("wrates"))
async def wrates(callback: types.CallbackQuery):
    splitted_data = callback.data.split("#")
    type = splitted_data[1]
    if type == "all":
        workers_rates = requests.get(SERVER_URL + f"/workers/rates/")

        if workers_rates.status_code != 200:
            return await callback.message.edit_text(
                "Ошибка сервера! Свяжитесь с тех.поддержкой @belofflab"
            )
        workers_rates_data = workers_rates.json()
        sorted_data = dict(
            sorted(workers_rates_data.items(), key=lambda item: item[1], reverse=True)
        )
        await callback.message.edit_text(
            "🌟<b>Рейтинг за весь период:</b>🌟\n\n"
            + "\n".join(
                [
                    f"💫 {name} {amount}₽"
                    if idx + 1 <= 1
                    else
                    f"{idx + 1}. {name} {amount}₽"
                    for idx, (name, amount) in enumerate(sorted_data.items())
                ]
            ),
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton(
                    text="За текущий месяц", callback_data="wrates#month"
                )
            ),
        )
    elif type == "month":
        today = datetime.date.today()
        first_day_of_month = today.replace(day=1)
        if today.month == 12:
            last_day_of_month = today.replace(
                year=today.year + 1, month=1, day=1
            ) - datetime.timedelta(days=1)
        else:
            last_day_of_month = today.replace(
                month=today.month + 1, day=1
            ) - datetime.timedelta(days=1)
        workers_rates = requests.get(
            SERVER_URL
            + f"/workers/rates/?date_range={first_day_of_month} {last_day_of_month}"
        )

        if workers_rates.status_code != 200:
            return await callback.message.edit_text(
                "Ошибка сервера! Свяжитесь с тех.поддержкой @belofflab"
            )
        workers_rates_data = workers_rates.json()
        sorted_data = dict(
            sorted(workers_rates_data.items(), key=lambda item: item[1], reverse=True)
        )
        await callback.message.edit_text(
            "🌟<b>Рейтинг за текущий месяц:</b>🌟\n\n"
            + "\n".join(
                [
                    f"💫 {name} {amount}₽"
                    if idx + 1 <= 1
                    else
                    f"{idx + 1}. {name} {amount}₽"
                    for idx, (name, amount) in enumerate(sorted_data.items())
                ]
            ),
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton(
                    text="За весь период", callback_data="wrates#all"
                )
            ),
        )
