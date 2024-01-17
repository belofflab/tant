import asyncio

from data.config import (QIWI_BILL_LIFETIME, QIWI_PAYMENT_ATTEMPT,
                         QIWI_PRIVATE_KEY, CHANNEL_ID)
from loader import bot
from pyqiwip2p import AioQiwiP2P
from pyqiwip2p.p2p_types import Bill

from database import models

async def create_bill(amount: float) -> Bill:
    async with AioQiwiP2P(QIWI_PRIVATE_KEY) as p2p:
        new_bill = await p2p.bill(amount=amount, lifetime=QIWI_BILL_LIFETIME)
    
    return new_bill

async def reject_payment(bill_id):
    async with AioQiwiP2P(QIWI_PRIVATE_KEY) as p2p:
        await p2p.reject(bill_id)

async def notify_rejected(**kwargs):pass

async def notify_expired(user_id, message_id, **kwargs): 
    await bot.edit_message_caption(chat_id=user_id, caption='Время на пополнение истекло', message_id=message_id)

async def notify_paid(user_id, service, client_info, message_id, **kwargs): 
    # await create_payment(user_id=user_id, amount=bill.amount)
    await models.Payment.create(
        user=user_id,
        service=int(service),
        input_info=client_info
    )
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=client_info.replace("Вы успешно оплатили", f"Пользователь {user_id} успешно оплатил")
    )
    await bot.edit_message_caption(
        caption=client_info,
        chat_id=user_id,
        message_id=message_id
    )

async def notify(response, user_id, message_id, bill, service, client_info):
    status = {
        'PAID': notify_paid,
        'EXPIRED': notify_expired, 
        'REJECTED': notify_rejected
    }
    await status[response.status](user_id=user_id, message_id=message_id, bill=bill, service=service, client_info=client_info)

async def wait_for_refill(bill: Bill, message_id: str, user_id: int, service: str, client_info: str):
     async with AioQiwiP2P(QIWI_PRIVATE_KEY) as p2p:
        response = await p2p.check(bill.bill_id)
        while response.status == 'WAITING':
            await asyncio.sleep(QIWI_PAYMENT_ATTEMPT)
            status = await p2p.check(bill.bill_id)
            response = status
        await notify(response, user_id, message_id, bill, service, client_info)