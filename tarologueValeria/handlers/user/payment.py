async def proceed_payment(message: types.Message,last_message_id, service: str, **kwargs) -> None:
    q_service = await models.Service.query.where(models.Service.idx == int(service)).gino.first()
    new_bill = await qiwi.create_bill(amount=q_service.amount)
    refill_balance_markup = await inline.refill_balance_keyboard(payment_url=new_bill.pay_url, bill_id=new_bill.bill_id, service=service)
    await message.delete()
    refill_message = await bot.edit_message_caption(
        chat_id=message.from_user.id,
        caption='Ожидание оплаты',
        message_id=last_message_id, 
        reply_markup=refill_balance_markup)
    
    client_info = """
Вы успешно оплатили "{service_name}"

Данные:

ФИО: {full_name}
Телефон: {mobile_phone}
Почта: {email}
""".format(
        user_id=message.from_user.id,
        service_name=q_service.name,
        **kwargs
)

    await qiwi.wait_for_refill(
            new_bill, 
            refill_message.message_id, 
            message.from_user.id, 
            service,
            client_info
        )

@dp.callback_query_handler(lambda c: c.data.startswith('cancel_payment'))
async def cancel_payment(callback: types.CallbackQuery):
    bill_id = callback.data.split('#')[1]
    service = callback.data.split('#')[2]
    await qiwi.reject_payment(bill_id)
    await show_service(callback=callback, service=service)


@dp.callback_query_handler(lambda c: c.data.startswith('about_me'))
async def about_me(callback: types.CallbackQuery):
    await callback.message.edit_caption("""
Изучаю ведическую астрологию с 2007 года. Консультирую с 2010 года. 

Провожу консультации лично, если Вы проживаете в городе  Омске или онлайн, если вы находитесь в любом уголке земли.
""", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='Назад', callback_data=inline.make_service_cd(level=0))))

