import requests
import typing as t
from aiogram import types
from loader import dp, bot
from decimal import Decimal
from states.admin_cashier import InputAmount
from data.config import SERVER_URL, BANNER
from filters.is_admin import IsAdmin
from aiogram.dispatcher import FSMContext
from keyboards.admin import inline

from .menu import admin


async def list_types(callback: types.CallbackQuery, **kwargs):
    await callback.message.edit_caption("Доступные манипуляции с кассой: ", reply_markup=await inline.cashier_keyboard())

async def input_amount(callback: types.CallbackQuery, type: str, state: FSMContext, **kwargs):

    translates = {
        "deposit": "пополнения",
        "withdrawal": "вывода",
    }

    await InputAmount.amount.set()
    new_message = await callback.message.edit_caption(f"Введите сумму для {translates[type]}: ", reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="cashier_move#cancel"
                    ),
                ),
            )
    await state.set_data({"last_message_id": new_message.message_id, "type": type, "attempt": 1})

@dp.message_handler(IsAdmin(), state=InputAmount.amount)
async def input_amount_amount(message: types.Message, state: FSMContext):
    translates = {
        "deposit": "пополнить",
        "withdrawal": "вывести",
    }
    async with state.proxy() as data:
        try:
            amount = Decimal(message.text)
            data["amount"] = amount
            await message.delete()
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Вы уверены, что хотите {translates[data['type']]} {amount}₽?",
                message_id=data["last_message_id"],
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Да", callback_data="cashier_move#confirm"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="cashier_move#cancel"
                    ),
                ),
            )
            data["last_message_id"] = new_message.message_id
        except:
            await message.delete()
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Сумма указана некорректно!\n\nПопытка: {data['attempt']}",
                message_id=data["last_message_id"],
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="cashier_move#cancel"
                    ),
                ),
            )
            data["last_message_id"] = new_message.message_id
            data["attempt"] = data["attempt"] + 1

@dp.callback_query_handler(IsAdmin(), lambda c:c.data.startswith("cashier_move"), state=InputAmount.amount)
async def cashier_move(callback: types.CallbackQuery, state: FSMContext):
    move = callback.data.split("#")[-1]
    if move == "confirm":
        async with state.proxy() as data:
            amount = data["amount"]
            type = data["type"]
        requests.post(SERVER_URL + "/admin/requests/", headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        },json={"amount": int(amount), "type": type})
        await state.finish()
        await admin(callback)
    else:
        await state.finish()
        await list_types(callback=callback)



@dp.callback_query_handler(IsAdmin(), inline.cashier_cd.filter())
async def cashier_navigate(callback: types.CallbackQuery, callback_data: dict,state: FSMContext) -> None:
    level = callback_data.get("level")
    type = callback_data.get("type")
    amount = callback_data.get("amount")

    levels = {
        "0": admin,
        "1": list_types,
        "2": input_amount,
    }

    current_level_function = levels[level]

    await current_level_function(callback, state=state, type=type, amount=amount)