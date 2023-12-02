import requests
import typing as t
from aiogram import types
from loader import dp, bot
from io import BytesIO
from data.config import SERVER_URL, BANNER
from aiogram.dispatcher import FSMContext
from keyboards.admin import inline
from states.admin_payment_detail import AdminPaymentDetail
from .menu import admin
from filters.is_admin import IsAdmin


@dp.callback_query_handler(IsAdmin(), lambda c:c.data.startswith("delete_payment_detail"))
async def change_payment_detail(callback: types.CallbackQuery):
    detail = callback.data.split("#")[-1]
    requests.delete(SERVER_URL + f"/admin/payment/details/{detail}")
    await list_payment_details(callback=callback)



async def list_payment_details(callback: types.CallbackQuery, **kwargs):
    response = requests.get(SERVER_URL + "/admin/payment/details/")
    details = response.json()
    await callback.message.edit_caption(
        caption="Доступные методы оплаты:\n"
        + "".join(
            [
                f"\n<b>{detail.get('name')}</b> : <code>{detail.get('text')}</code>"
                for detail in details
            ]
        ),
        reply_markup=await inline.payment_details_keyboard(),
    )

async def show_payment_details(callback: types.CallbackQuery, detail: str, **kwargs):
    response = requests.get(SERVER_URL + f"/admin/payment/details/{detail}")
    s_detail = response.json()
    await callback.message.edit_caption(caption=f"""
Ключ: <b>{s_detail.get("name")}</b>
Реквизит: <b>{s_detail.get("text")}</b>
""", reply_markup=await inline.show_payment_detail_keyboard(detail=detail))

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "add_payment_detail")
async def add_payment_detail(
    callback: types.CallbackQuery, state: FSMContext, **kwargs
):
    new_message = await callback.message.edit_caption(
        caption="Укажите наименование",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="add_payment_detail_decline"
            )
        ),
    )
    await state.set_data({"last_message_id": new_message.message_id})

    await AdminPaymentDetail.name.set()


@dp.callback_query_handler(IsAdmin(), 
    lambda c: c.data.startswith("add_payment_detail_back"),
    state=AdminPaymentDetail.all_states,
)
async def add_payment_detail_back(callback: types.CallbackQuery, state: FSMContext):
    w = callback.data.split("#")[-1]
    back_w = {"name": add_payment_detail, "text": add_payment_detail_name}
    await back_w[w](callback=callback, message=callback, state=state)


@dp.callback_query_handler(IsAdmin(), 
    lambda c: c.data == "add_payment_detail_decline",
    state=AdminPaymentDetail.all_states,
)
async def add_payment_detail_decline(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await list_payment_details(callback=callback)


@dp.message_handler(IsAdmin(), state=AdminPaymentDetail.name)
async def add_payment_detail_name(
    message: t.Union[types.Message, types.CallbackQuery], state: FSMContext, **kwargs
):
    async with state.proxy() as data:
        if isinstance(message, types.Message):
            data["name"] = message.text
            await message.delete()
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"<b>Наимнование:</b>{message.text}\n\nХорошо. Теперь укажите сами реквизиты",
                message_id=data.get("last_message_id"),
                reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
                    types.InlineKeyboardButton(
                        text="Назад", callback_data="add_payment_detail_back#name"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="add_payment_detail_decline"
                    ),
                ),
            )
        elif isinstance(message, types.CallbackQuery):
            message: types.CallbackQuery
            new_message = await message.message.edit_caption(
                caption=f"<b>Наимнование:</b>{data['name']}\n\nХорошо. Теперь укажите сами реквизиты",
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Назад", callback_data="add_payment_detail_back#name"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="add_payment_detail_decline"
                    ),
                ),
            )
        data["last_message_id"] = new_message.message_id

    await AdminPaymentDetail.text.set()


@dp.message_handler(IsAdmin(), state=AdminPaymentDetail.text)
async def add_payment_detail_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        await message.delete()
        new_message = await bot.edit_message_caption(
            chat_id=message.from_user.id,
            caption=f"<b>Наимнование: </b>{data['name']}\n<b>Реквизиты: </b>{message.text}\n\nВы уверены что хотите сохранить?",
            message_id=data["last_message_id"],
            reply_markup=await inline.payment_details_confirm_keyboard(),
        )
        data["last_message_id"] = new_message.message_id


@dp.callback_query_handler(IsAdmin(), 
    lambda c: c.data == "add_payment_detail_confirm",
    state=AdminPaymentDetail.all_states,
)
async def add_payment_detail_confirm(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data["name"]
        text = data["text"]

    requests.post(
        SERVER_URL + "/admin/payment/details/",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={"name": name, "text": text},
    )

    await state.finish()
    await list_payment_details(callback=callback)


@dp.callback_query_handler(IsAdmin(), inline.payment_details_cd.filter())
async def payment_details_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    detail = callback_data.get("detail")

    levels = {
        "0": admin,
        "1": list_payment_details,
        "2": show_payment_details,
    }

    current_level_function = levels[level]

    await current_level_function(callback, detail=detail)
