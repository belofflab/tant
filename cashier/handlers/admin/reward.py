async def penalty_worker(callback: types.CallbackQuery, worker: str, state: FSMContext):
    new_message = await callback.message.edit_caption(
        caption="Введите сумму для списания: ",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data="worker_penalty#cancel"
            ),
        ),
    )
    await penaltyState.amount.set()
    await state.set_data(
        {
            "last_message_id": new_message.message_id,
            "penalty_attempt": 1,
            "worker": worker,
        }
    )


@dp.message_handler(IsAdmin(), state=penaltyState.amount)
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


@dp.callback_query_handler(IsAdmin(), 
    lambda c: c.data.startswith("worker_penalty"), state=penaltyState.amount
)
async def worker_penalty(callback: types.CallbackQuery, state: FSMContext):
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

