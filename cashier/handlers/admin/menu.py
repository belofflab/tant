import requests
import typing as t
from aiogram import types
from loader import dp, bot
from io import BytesIO
from decimal import Decimal
from states.refill import RefillState
from states.debit import DebitState
from states.reward import RewardState
from states.penalty import PenaltyState
from data.config import SERVER_URL, BANNER
from aiogram.dispatcher import FSMContext
from filters.is_admin import IsAdmin
from keyboards.admin import inline


@dp.message_handler(IsAdmin(), commands="admin")
async def admin(message: t.Union[types.Message, types.CallbackQuery], **kwargs):
    response = requests.get(
        SERVER_URL + "/admin/info/",
    )
    workers_response = requests.get(SERVER_URL + "/workers/")
    workers = workers_response.json()
    if response.status_code != 200:
        return await message.answer(
            "Проблема на сервере, обратитесь к техническому администратору"
        )
    data = response.json()
    if isinstance(message, types.Message):
        await message.answer_photo(
            photo=types.InputFile(BANNER),
            caption="""
Общий доход: <b>{total}₽</b>
Маржа: <b>{marginal}₽</b>
Долг воркерам: <b>{owed}₽</b>

<b>Работники:</b>
""".format(
                **data
            )
            + "\n".join(
                [
                    f"{worker.get('name')} : {worker.get('amount')}₽"
                    for worker in workers
                ]
            ),
            reply_markup=await inline.admin_keyboard(),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        await message.message.edit_caption(
            """
Общий доход: <b>{total}₽</b>
Маржа: <b>{marginal}₽</b>
Долг воркерам: <b>{owed}₽</b>

<b>Работники:</b>
""".format(
                **data
            )
            + "\n".join(
                [
                    f"{worker.get('name')} : {worker.get('amount')}₽"
                    for worker in workers
                ]
            ),
            reply_markup=await inline.admin_keyboard(),
        )


async def list_workers(callback: types.CallbackQuery, page: str, **kwargs):
    await callback.message.edit_caption(
        "Активные воркеры: ",
        reply_markup=await inline.workers_keyboard(current_page=page),
    )


async def list_workers_requests(callback: types.CallbackQuery, page: str, **kwargs):
    await callback.message.edit_caption(
        "Чеки (От самых новых):\n\n📈- Пополнение\n📉- Вывод",
        reply_markup=await inline.workers_requests_keyboard(current_page=page),
    )


async def show_workers_request(
    callback: types.CallbackQuery, request: str, page: str, **kwargs
):
    response = requests.get(SERVER_URL + f"/worker/requests/{request}")
    data = response.json()
    await callback.message.edit_caption(
        caption=f"""
Работник: @{data['worker']['username']}

Чек на сумму: {data.get("amount")}₽
Наша прибыль: {data.get("marginal_amount")}₽

Статус: <b>{'✅ Одобрена' if data.get("is_success") else '❌ Отклонена'}</b>

Тип: <b>{"Депозит" if data.get("type") == "deposit" else "Вывод"}</b>

""",
        reply_markup=await inline.show_worker_request_keyboard(
            page=page, request=request
        ),
    )


@dp.callback_query_handler(IsAdmin(), lambda c: c.data.startswith("show_receipt"))
async def show_receipt(callback: types.CallbackQuery):
    receipt = callback.data.split("#")[-1]
    response = requests.get(SERVER_URL + f"/worker/requests/{receipt}")
    data = response.json()
    if data.get("receipt") is None:
        return
    document = requests.get(SERVER_URL.replace("/api/v1", "/") + data.get("receipt"))
    document_extension = data.get("receipt").split(".")[-1]
    await bot.send_document(
        chat_id=callback.from_user.id,
        document=types.InputFile(
            BytesIO(document.content), filename=f"receipt.{document_extension}"
        ),
    )


async def show_worker(callback: types.CallbackQuery, worker: str, page: str, **kwargs):
    response = requests.get(SERVER_URL + f"/workers/{worker}")
    data = response.json()
    await callback.message.edit_caption(
        caption=f"""
Пользователь: <b>{data.get("name")} (@{data.get("username")})</b>
Баланс: <b>{data.get("amount")}₽</b>

""",
        reply_markup=await inline.show_worker_keyboard(worker=worker, page=page),
    )


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("deposit_request_confirm")
)
async def deposit_request_confirm(callback: types.CallbackQuery):
    request_id = int(callback.data.split("#")[-1])

    response = requests.patch(
        SERVER_URL + "/worker/requests/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": request_id,
            "is_success": True,
            "comment": "string",
        },
    )
    response_data = response.json()
    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n✅ Одобрена"
    )
    await bot.send_message(
        chat_id=response_data["worker"]["id"],
        text=f"Ваша заявка на пополнение {response_data['amount']} одобрена! Было начислено {response_data['worker_amount']} с учётом комиссии.\n\nЧтобы обновить баланс жите: /start",
    )


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("deposit_request_decline")
)
async def deposit_request_decline(callback: types.CallbackQuery):
    request_id = int(callback.data.split("#")[-1])

    response = requests.patch(
        SERVER_URL + "/worker/requests/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": request_id,
            "is_success": False,
            "comment": "string",
        },
    )
    response_data = response.json()
    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n❌ Отклонена"
    )
    await bot.send_message(
        chat_id=response_data["worker"]["id"],
        text=f"Ваша заявка на пополнение {response_data['amount']} отклонена!\n\nЧтобы обновить баланс жите: /start",
    )


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("withdrawal_request_confirm")
)
async def deposit_request_confirm(callback: types.CallbackQuery):
    request_id = int(callback.data.split("#")[-1])

    response = requests.patch(
        SERVER_URL + "/worker/requests/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": request_id,
            "is_success": True,
            "comment": "string",
        },
    )
    response_data = response.json()
    await callback.message.edit_text(text=f"{callback.message.text}\n\n✅ Одобрена")
    await bot.send_message(
        chat_id=response_data["worker"]["id"],
        text=f"Ваша заявка на вывод {response_data['amount']} одобрена!\n\nВывод будет доставлен в ближайшее время!\n\nЧтобы обновить баланс жите: /start",
    )


async def refill_worker(callback: types.CallbackQuery, worker: str, state: FSMContext):
    new_message = await callback.message.edit_caption(
        caption="Введите сумму для пополнения: ",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="worker_refill#cancel"
            ),
        ),
    )
    await RefillState.amount.set()
    await state.set_data(
        {
            "last_message_id": new_message.message_id,
            "refill_attempt": 1,
            "worker": worker,
        }
    )


@dp.message_handler(IsAdmin(), state=RefillState.amount)
async def refill_worker_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            amount = Decimal(message.text)
            data["amount"] = amount
            await message.delete()
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Вы уверены, что хотите пополнить работнику баланс на {amount}₽",
                message_id=data["last_message_id"],
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Да", callback_data="worker_refill#confirm"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="worker_refill#cancel"
                    ),
                ),
            )
            data["last_message_id"] = new_message.message_id
        except:
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Сумма указана некорректно!\n\nПопытка: {data['refill_attempt']}",
                message_id=data["last_message_id"],
            )
            data["last_message_id"] = new_message.message_id
            data["refill_attempt"] = data["refill_attempt"] + 1


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("worker_refill"), state=RefillState.amount
)
async def worker_refill(callback: types.CallbackQuery, state: FSMContext):
    do = callback.data.split("#")[-1]
    async with state.proxy() as data:
        if do == "confirm":
            await state.finish()
            # requests.post(
            #     SERVER_URL + "/workers/fill/",
            #     headers={
            #         "accept": "application/json",
            #         "Content-Type": "application/json",
            #     },
            #     json={"id": data["worker"], "amount": int(data["amount"])},
            # )
            requests.post(
                SERVER_URL
                + f"/worker/requests/?worker={data['worker']}&amount={data['amount']}&type=deposit&is_admin=true"
            )
            await show_worker(callback=callback, worker=data["worker"], page=1)
        elif do == "cancel":
            await state.finish()
            await show_worker(callback=callback, worker=data["worker"], page=1)


async def debit_worker(callback: types.CallbackQuery, worker: str, state: FSMContext):
    new_message = await callback.message.edit_caption(
        caption="Введите сумму для списания: ",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="worker_debit#cancel"
            ),
        ),
    )
    await DebitState.amount.set()
    await state.set_data(
        {
            "last_message_id": new_message.message_id,
            "debit_attempt": 1,
            "worker": worker,
        }
    )


@dp.message_handler(IsAdmin(), state=DebitState.amount)
async def debit_worker_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            amount = Decimal(message.text)
            data["amount"] = amount
            await message.delete()
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Вы уверены, что хотите списать работнику баланс на {amount}₽",
                message_id=data["last_message_id"],
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Да", callback_data="worker_debit#confirm"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="worker_debit#cancel"
                    ),
                ),
            )
            data["last_message_id"] = new_message.message_id
        except:
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Сумма указана некорректно!\n\nПопытка: {data['debit_attempt']}",
                message_id=data["last_message_id"],
            )
            data["last_message_id"] = new_message.message_id
            data["debit_attempt"] = data["debit_attempt"] + 1


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("worker_debit"), state=DebitState.amount
)
async def worker_debit(callback: types.CallbackQuery, state: FSMContext):
    do = callback.data.split("#")[-1]
    async with state.proxy() as data:
        if do == "confirm":
            await state.finish()
            # requests.post(
            #     SERVER_URL + "/workers/fill/",
            #     headers={
            #         "accept": "application/json",
            #         "Content-Type": "application/json",
            #     },
            #     json={"id": data["worker"], "amount": -int(data["amount"])},
            # )
            requests.post(
                SERVER_URL
                + f"/worker/requests/?worker={data['worker']}&amount={data['amount']}&type=withdrawal&is_admin=true"
            )
            await show_worker(callback=callback, worker=data["worker"], page=1)
        elif do == "cancel":
            await state.finish()
            await show_worker(callback=callback, worker=data["worker"], page=1)


async def delete_worker(callback: types.CallbackQuery, worker: str, state: FSMContext):
    await callback.message.edit_caption(
        "Вы действительно хотите удалить сотрудника?",
        reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton(
                text="Да", callback_data=f"delete_worker#confirm#{worker}"
            ),
            types.InlineKeyboardButton(
                text="Отмена", callback_data=f"delete_worker#cancel#{worker}"
            ),
        ),
    )


@dp.callback_query_handler(IsAdmin(), lambda c: c.data.startswith("delete_worker"))
async def delete_worker_confirm(callback: types.CallbackQuery):
    splitted_data = callback.data.split("#")
    do = splitted_data[1]
    worker = splitted_data[2]
    if do == "confirm":
        requests.post(SERVER_URL + f"/workers/disable/{worker}")
        await list_workers(callback=callback, page=1)
    elif do == "cancel":
        await show_worker(callback=callback, worker=worker, page=1)


async def reward_worker(callback: types.CallbackQuery, worker: str, state: FSMContext):
    new_message = await callback.message.edit_caption(
        caption="Введите сумму поощрения: ",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="worker_reward#cancel"
            ),
        ),
    )
    await RewardState.amount.set()
    await state.set_data(
        {
            "last_message_id": new_message.message_id,
            "reward_attempt": 1,
            "worker": worker,
        }
    )


@dp.message_handler(IsAdmin(), state=RewardState.amount)
async def reward_worker_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            amount = Decimal(message.text)
            data["amount"] = amount
            await message.delete()
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Вы уверены, что хотите пополнить работнику баланс на {amount}₽",
                message_id=data["last_message_id"],
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Да", callback_data="worker_reward#confirm"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="worker_reward#cancel"
                    ),
                ),
            )
            data["last_message_id"] = new_message.message_id
        except:
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Сумма указана некорректно!\n\nПопытка: {data['reward_attempt']}",
                message_id=data["last_message_id"],
            )
            data["last_message_id"] = new_message.message_id
            data["reward_attempt"] = data["reward_attempt"] + 1


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("worker_reward"), state=RewardState.amount
)
async def worker_reward(callback: types.CallbackQuery, state: FSMContext):
    do = callback.data.split("#")[-1]
    async with state.proxy() as data:
        if do == "confirm":
            await state.finish()
            requests.post(
                SERVER_URL + "/admin/reward/",
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "worker": data["worker"],
                    "amount": int(data["amount"]),
                    "is_admin": False,
                    "type": "deposit",
                },
            )
            await show_worker(callback=callback, worker=data["worker"], page=1)
        elif do == "cancel":
            await state.finish()
            await show_worker(callback=callback, worker=data["worker"], page=1)


async def penalty_worker(callback: types.CallbackQuery, worker: str, state: FSMContext):
    new_message = await callback.message.edit_caption(
        caption="Введите сумму штрафа: ",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="worker_penalty#cancel"
            ),
        ),
    )
    await PenaltyState.amount.set()
    await state.set_data(
        {
            "last_message_id": new_message.message_id,
            "penalty_attempt": 1,
            "worker": worker,
        }
    )


@dp.message_handler(IsAdmin(), state=PenaltyState.amount)
async def penalty_worker_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            amount = Decimal(message.text)
            data["amount"] = amount
            await message.delete()
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Вы уверены, что хотите списать работнику баланс на {amount}₽",
                message_id=data["last_message_id"],
                reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                    types.InlineKeyboardButton(
                        text="Да", callback_data="worker_penalty#confirm"
                    ),
                    types.InlineKeyboardButton(
                        text="Отмена", callback_data="worker_penalty#cancel"
                    ),
                ),
            )
            data["last_message_id"] = new_message.message_id
        except:
            new_message = await bot.edit_message_caption(
                chat_id=message.from_user.id,
                caption=f"Сумма указана некорректно!\n\nПопытка: {data['penalty_attempt']}",
                message_id=data["last_message_id"],
            )
            data["last_message_id"] = new_message.message_id
            data["penalty_attempt"] = data["penalty_attempt"] + 1


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("worker_penalty"), state=PenaltyState.amount
)
async def worker_penalty(callback: types.CallbackQuery, state: FSMContext):
    do = callback.data.split("#")[-1]
    async with state.proxy() as data:
        if do == "confirm":
            await state.finish()
            requests.post(
                SERVER_URL + "/admin/penalty/",
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "worker": data["worker"],
                    "amount": int(data["amount"]),
                    "is_admin": False,
                    "type": "withdrawal",
                },
            )
            await show_worker(callback=callback, worker=data["worker"], page=1)
        elif do == "cancel":
            await state.finish()
            await show_worker(callback=callback, worker=data["worker"], page=1)


@dp.callback_query_handler(IsAdmin(), lambda c: c.data.startswith("worker_move"))
async def worker_move(callback: types.CallbackQuery, state: FSMContext):
    splitted_cd = callback.data.split("#")
    move = splitted_cd[1]
    worker = splitted_cd[2]
    moves = {
        "refill": refill_worker,
        "debit": debit_worker,
        "reward": reward_worker,
        "penalty": penalty_worker,
        "delete": delete_worker,
    }

    await moves[move](callback, worker, state)


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("withdrawal_request_decline")
)
async def deposit_request_decline(callback: types.CallbackQuery):
    request_id = int(callback.data.split("#")[-1])

    response = requests.patch(
        SERVER_URL + "/worker/requests/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": request_id,
            "is_success": False,
            "comment": "string",
        },
    )
    response_data = response.json()
    await callback.message.edit_text(text=f"{callback.message.text}\n\n❌ Отклонена")
    await bot.send_message(
        chat_id=response_data["worker"]["id"],
        text=f"Ваша заявка на вывод {response_data['amount']} отклонена!\n\nЧтобы обновить баланс жите: /start",
    )


@dp.callback_query_handler(IsAdmin(), inline.workers_cd.filter())
async def workers_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    worker = callback_data.get("worker")
    page = callback_data.get("page")

    levels = {
        "0": admin,
        "1": list_workers,
        "2": show_worker,
    }

    current_level_function = levels[level]

    await current_level_function(callback, page=page, worker=worker)


@dp.callback_query_handler(IsAdmin(), inline.workers_requests_cd.filter())
async def workers_requests_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    request = callback_data.get("request")
    page = callback_data.get("page")

    levels = {
        "0": admin,
        "1": list_workers_requests,
        "2": show_workers_request,
    }

    current_level_function = levels[level]

    await current_level_function(callback, request=request, page=page)
