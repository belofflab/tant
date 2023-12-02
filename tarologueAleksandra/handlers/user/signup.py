@dp.callback_query_handler(lambda c: c.data.startswith('signup'))
async def signup(callback: types.CallbackQuery, state: FSMContext):
    service = callback.data.split('#')[-1]
    markup = await inline.signup_cancel_keyboard(service=service)
    await SignupState.full_name.set()

    async with state.proxy() as data:
        data['service'] = service

        message = await callback.message.edit_caption(caption='Введите ФИО: ', reply_markup=markup)

        data['last_message_id'] = message.message_id

@dp.message_handler(state=SignupState.full_name)
async def signup_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
        markup = await inline.signup_cancel_keyboard(service=data['service'])
        await message.delete()
        message = await bot.edit_message_caption(
            chat_id=message.from_user.id,
            caption=f'<b>ФИО:</b> {data["full_name"]}\n\nВведите номер',
            message_id=data['last_message_id'],
            reply_markup=markup
        )
        data['last_message_id'] = message.message_id

    await SignupState.mobile_phone.set()
    
@dp.message_handler(state=SignupState.mobile_phone)
async def signup_mobile_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mobile_phone'] = message.text

        markup = await inline.signup_cancel_keyboard(service=data['service'])
        await message.delete()
        message = await bot.edit_message_caption(
            chat_id=message.from_user.id,
            caption=f'<b>ФИО:</b> {data["full_name"]}\n<b>Телефон:</b> {data["mobile_phone"]}\n\nВведите почту',
            message_id=data['last_message_id'],
            reply_markup=markup
        )
        data['last_message_id'] = message.message_id

    await SignupState.email.set()

@dp.message_handler(state=SignupState.email)
async def signup_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        service = data['service']
        full_name = data['full_name']
        mobile_phone = data['mobile_phone']
        email = data['email']
        await state.finish()
        await proceed_payment(
            message=message,
            last_message_id=data['last_message_id'],
            service=service,
            full_name=full_name,
            mobile_phone=mobile_phone,
            email=email
        )

@dp.callback_query_handler(lambda c: c.data.startswith('signup_cancel'), state=SignupState.all_states)
async def signup_cancel(callback: types.CallbackQuery, state: FSMContext):
    service = callback.data.split('#')[-1]

    await state.finish()

    await show_service(callback=callback, service=service)

