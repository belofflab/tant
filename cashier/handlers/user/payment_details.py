import requests
import typing as t
from aiogram import types
from loader import dp, bot
from io import BytesIO
from data.config import SERVER_URL, BANNER
from aiogram.dispatcher import FSMContext
from keyboards.user import inline
from states.cuser_payment_detail import CUserPaymentDetail
from .menu import start


@dp.callback_query_handler(lambda c:c.data.startswith("delete_user_payment_detail"))
async def change_payment_detail(callback: types.CallbackQuery):
    detail = callback.data.split("#")[-1]
    requests.delete(SERVER_URL + f"/users/payment/details/{detail}")
    await list_payment_details(callback=callback)



async def list_payment_details(callback: types.CallbackQuery, **kwargs):
    response = requests.get(SERVER_URL + f"/users/{callback.from_user.id}/payment/details/")
    details = response.json()
    await callback.message.edit_text(
        text="Доступные методы оплаты:\n"
        + "".join(
            [
                f"\n<b>{detail.get('name')}</b> : <code>{detail.get('text')}</code>"
                for detail in details
            ]
        ),
        reply_markup=await inline.payment_details_keyboard(callback.from_user.id),
    )

async def show_payment_details(callback: types.CallbackQuery, detail: str, **kwargs):
    response = requests.get(SERVER_URL + f"/users/payment/details/?id={detail}")
    s_detail = response.json()
    await callback.message.edit_text(text=f"""
Ключ: <b>{s_detail.get("name")}</b>
Реквизит: <b>{s_detail.get("text")}</b>
""", reply_markup=await inline.show_payment_detail_keyboard(detail=detail))

@dp.callback_query_handler(lambda c: c.data == "add_user_payment_detail")
async def add_payment_detail(
    callback: types.CallbackQuery, state: FSMContext, **kwargs
):
    new_message = await callback.message.edit_text(
        text="Укажите наименование",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="add_user_payment_detail_decline"
            )
        ),
    )
    await state.set_data({"last_message_id": new_message.message_id})

    await CUserPaymentDetail.name.set()


@dp.callback_query_handler(
    lambda c: c.data.startswith("add_user_payment_detail_back"),
    state=CUserPaymentDetail.all_states,
)
async def add_payment_detail_back(callback: types.CallbackQuery, state: FSMContext):
    w = callback.data.split("#")[-1]
    back_w = {"name": add_payment_detail, "text": add_payment_detail_name}
    await back_w[w](callback=callback, message=callback, state=state)


@dp.callback_query_handler(
    lambda c: c.data == "add_user_payment_detail_decline",
    state=CUserPaymentDetail.all_states,
)
async def add_payment_detail_decline(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await list_payment_details(callback=callback)


@dp.message_handler(state=CUserPaymentDetail.name)
async def add_payment_detail_name(
    message: t.Union[types.Message, types.CallbackQuery], state: FSMContext, **kwargs
):
    async with state.proxy() as data:
        if isinstance(message, types.Message):
            data["name"] = message.text
            await message.delete()
            new_message = await bot.edit_message_text(
                chat_id=message.from_user.id,
                text=f"<b>Наимнование:</b>{message.text}\n\nХорошо. Теперь укажите сами реквизиты",
                message_id=data.get("last_message_id"),
                reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
                    types.InlineKeyboardButton(
                        text="Назад", callback_data="add_user_payment_detail_back#name"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="add_user_payment_detail_decline"
                    ),
                ),
            )
        elif isinstance(message, types.CallbackQuery):
            message: types.CallbackQuery
            new_message = await message.message.edit_text(
                text=f"<b>Наимнование:</b>{data['name']}\n\nХорошо. Теперь укажите сами реквизиты",
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Назад", callback_data="add_user_payment_detail_back#name"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="add_user_payment_detail_decline"
                    ),
                ),
            )
        data["last_message_id"] = new_message.message_id

    await CUserPaymentDetail.text.set()


@dp.message_handler(state=CUserPaymentDetail.text)
async def add_payment_detail_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        await message.delete()
        new_message = await bot.edit_message_text(
            chat_id=message.from_user.id,
            text=f"<b>Наимнование: </b>{data['name']}\n<b>Реквизиты: </b>{message.text}\n\nВы уверены что хотите сохранить?",
            message_id=data["last_message_id"],
            reply_markup=await inline.payment_details_confirm_keyboard(),
        )
        data["last_message_id"] = new_message.message_id


@dp.callback_query_handler(
    lambda c: c.data == "add_user_payment_detail_confirm",
    state=CUserPaymentDetail.all_states,
)
async def add_payment_detail_confirm(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data["name"]
        text = data["text"]

    requests.post(
        SERVER_URL + "/users/payment/details/",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={"user": callback.from_user.id, "name": name, "text": text},
    )

    await state.finish()
    await list_payment_details(callback=callback)


@dp.callback_query_handler(inline.user_payment_details_cd.filter())
async def payment_details_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    detail = callback_data.get("detail")

    levels = {
        "0": start,
        "1": list_payment_details,
        "2": show_payment_details,
    }

    current_level_function = levels[level]

    await current_level_function(callback, detail=detail)
