import requests
import typing as t
from aiogram import types
from loader import dp, bot
from io import BytesIO
from data.config import SERVER_URL, BANNER
from aiogram.dispatcher import FSMContext
from keyboards.admin import inline
from states.total_conversion import TotalConversionState
from .menu import admin
from filters.is_admin import IsAdmin


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "total_conversion")
async def total_conversion(callback: types.CallbackQuery, state: FSMContext):
    new_message = await callback.message.edit_caption(
        "Введите период в формате <b>10.10.2023</b> <b>10.12.2023</b>",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="total_conversion_cancel"
            )
        ),
    )
    await TotalConversionState.date_range.set()
    await state.set_data({"last_message_id": new_message.message_id})


@dp.message_handler(
    regexp=r"\d{2}.\d{2}.\d{4} \d{2}.\d{2}.\d{4}", state=TotalConversionState.date_range
)
async def total_conversion_date_range(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        last_message_id = data["last_message_id"]
        date_range = message.text
        await message.delete()
        headers = {
            "accept": "application/json",
        }

        params = {
            "date_range": date_range,
        }

        response = requests.get(
            SERVER_URL + "/analytics/total/conversion", params=params, headers=headers
        )
        data = response.json()

        def proceed_workers(workers):
            return "\n".join(
                [
                    f"<b>{worker} ({worker_data['len']}Ч)</b> {worker_data['sum1']}₽ (~{worker_data['avg']}₽) ({worker_data['sum3']}₽) (наши {worker_data['sum2']}₽)"
                    for worker, worker_data in workers.items()
                ]
            )

        new_message = await bot.edit_message_caption(
            chat_id=message.from_user.id,
            caption=f"""
Период: <b>{date_range}</b>

Приход: <b>{data.get('total')}₽</b>
Маржа: <b>{data.get('marginal')}₽</b>
Количество чеков: <b>{data.get('total_requests')}</b>

{proceed_workers(data.get('workers'))}

Вы также можете ещё раз указать период в формате <b>10.10.2023</b> <b>10.12.2023</b>
""",
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton(
                    text="Отмена", callback_data="total_conversion_cancel"
                )
            ),
            message_id=last_message_id,
        )
        data["last_message_id"] = new_message.message_id


@dp.callback_query_handler(
    IsAdmin(),
    lambda c: c.data == "total_conversion_cancel",
    state=TotalConversionState.date_range,
)
async def total_conversion_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await admin(message=callback)
