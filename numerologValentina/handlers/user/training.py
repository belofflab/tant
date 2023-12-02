import requests
import datetime
from typing import Union

from aiogram import types
import os
import uuid
from data.config import SERVER_URL, CHANNEL_ID, BASE_DIR, TRAINING_CHANNEL
from math import ceil
from database import models
from keyboards.user import inline
from aiogram.dispatcher import FSMContext
from states.training_buy import TrainingBuy
from io import BytesIO
from data.config import TRAINING_CHANNEL
from loader import dp, bot
from .menu import start

TRAINING_COST = 8000
WORKER_NAME = "Валентине"
WORKER_ID = 6933270743
WORKER_USERNAME = "valentina_numerologEnerg"
TRAINING_DESCRIPTION="""
<b>Кому подойдёт это обучение👇?</b>

Вас тянет эзотерика, таро и вы хотите раскрыть своё предназначение и найти дело для души .

Вы уже пытались обучаться самостоятельно, но так и не поняли как работает таро

Вы хотите освоить новое дело, помогать людям и дополнительно зарабатывать

<b>Что вы получите на обучении </b>

Систему и алгоритм изучения таро 

Обратную связь в течении трёх недель после обретения обучения

<b>ПРАКТИКУ РАСКЛАДОВ ( триплет ) </b>
Это поможет закрепить навык чтения карт и обрести уверенность в своих трактовках

Если у вас остались вопросы можете задать здесь ⤵️

@{worker}
"""


async def get_or_buy_course(callback: types.CallbackQuery, worker: str, **kwargs):
    is_active_subscription = False
    now = datetime.datetime.now()
    training = await models.TaroTraining.query.where(
        models.TaroTraining.user == callback.from_user.id
    ).gino.first()
    if training is not None:
        if now < training.end_date:
            is_active_subscription = True
    new_link = await bot.create_chat_invite_link(
        chat_id=TRAINING_CHANNEL,
        expire_date=now + datetime.timedelta(minutes=30),
        member_limit=1,
    )
    await callback.message.edit_caption(
        caption=TRAINING_DESCRIPTION.format(worker=worker),
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(text="Смотреть курс", url=new_link.invite_link)
            if is_active_subscription
            else types.InlineKeyboardButton(
                text="Купить",
                callback_data=f"buy_training#{worker}",
            ),
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_training_cd(level=0, worker=worker),
            ),
        ),
    )


@dp.callback_query_handler(
    lambda c: c.data.startswith("menu_order_training"), state=TrainingBuy.receipt
)
async def order_training_cancel(callback: types.CallbackQuery, state: FSMContext):
    worker = callback.data.split("#")[-1]
    await state.finish()
    await start(message=callback, worker=worker)

@dp.callback_query_handler(
    lambda c: c.data.startswith("menu_order_training")
)
async def order_training_cancel(callback: types.CallbackQuery, state: FSMContext):
    worker = callback.data.split("#")[-1]
    await state.finish()
    await start(message=callback, worker=worker)


@dp.callback_query_handler(lambda c: c.data.startswith("training_request_confirm"))
async def training_request_confirm(callback: types.CallbackQuery):
    wrequest_id = int(callback.data.split("#")[1])
    last_message_id = int(callback.data.split("#")[2])
    user_id = int(callback.data.split("#")[3])
    worker = WORKER_USERNAME

    response = requests.patch(
        SERVER_URL + "/worker/requests/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": wrequest_id,
            "is_success": True,
            "comment": "string",
        },
    )
    response_data = response.json()
    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n✅ Одобрена"
    )

    training = await models.TaroTraining.query.where(
        models.TaroTraining.user == user_id
    ).gino.first()
    if training is None:
        await models.TaroTraining.create(user=user_id)
    else:
        now = datetime.datetime.now()
        await bot.unban_chat_member(
            TRAINING_CHANNEL, user_id=user_id, only_if_banned=True
        )
        await training.update(
            start_date=now, end_date=now + datetime.timedelta(days=90), is_banned=False
        ).apply()

    await bot.edit_message_caption(
        chat_id=user_id,
        message_id=last_message_id,
        caption="<b>Заявка на покупку обучения одобрена!</b>\n\nПерейдите в личный кабинет",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Обучение 🔥",
                callback_data=inline.make_training_cd(
                    level=1,
                    worker=worker,
                ),
            ),
            types.InlineKeyboardButton(
                text="В главное меню", callback_data=inline.make_training_cd(level=0)
            ),
        ),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("training_request_decline"))
async def training_request_decline(callback: types.CallbackQuery):
    mrequest_id = int(callback.data.split("#")[1])
    wrequest_id = int(callback.data.split("#")[1])
    last_message_id = int(callback.data.split("#")[2])
    user_id = int(callback.data.split("#")[3])
    worker = WORKER_USERNAME

    response = requests.patch(
        SERVER_URL + "/worker/requests/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": wrequest_id,
            "is_success": False,
            "comment": "string",
        },
    )
    response_data = response.json()
    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n❌ Отклонена"
    )
    await bot.edit_message_caption(
        chat_id=user_id,
        caption="Ваша заявка на покупку обучения Таро отклонена",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="В главное меню", callback_data=inline.make_training_cd(level=0)
            ),
        ),
        message_id=last_message_id,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("buy_training"))
async def buy_training(callback: types.CallbackQuery):
    worker = callback.data.split("#")[1]
    await callback.message.edit_caption(
        caption=f"""
Оплатите по реквизитам: <code>4276673835364343</code>

<b>Получатель:</b> Сергей Андреевич К.
<b>Банк:</b> Сбербанк.

Сумма: <b><del>12000</del></b> <code>{TRAINING_COST}</code>₽

После оплаты нажмите кнопку <b>Подтвердить</b> и прикрепите чек в формате скриншота.
""",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Подтвердить", callback_data=f"confirm_buy_training#{worker}"
            ),
            types.InlineKeyboardButton(
                text="Отмена", callback_data=f"menu_order_training#{worker}"
            ),
        ),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("confirm_buy_training"))
async def buy_training_confirm(callback: types.CallbackQuery, state: FSMContext):
    worker = callback.data.split("#")[1]
    new_message = await callback.message.edit_caption(
        "Отправьте чек в формате скриншота",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data=f"menu_order_training#{worker}"
            )
        ),
    )
    await TrainingBuy.receipt.set()
    await state.set_data({"last_message_id": new_message.message_id, "worker": worker})


@dp.message_handler(
    content_types=[types.ContentType.DOCUMENT, types.ContentType.PHOTO],
    state=TrainingBuy.receipt,
)
async def control_amount(message: types.Message, state: FSMContext) -> None:
    amount = TRAINING_COST
    document = message.document
    photo = message.photo
    last_message_id = await state.get_data("last_message_id")
    photo_to_delete = None
    if isinstance(document, types.Document):
        file_extension = os.path.splitext(document.file_name)[1]
        unique_filename = str(uuid.uuid4()) + file_extension
        file_info = await bot.get_file(document.file_id)
        file_path = file_info.file_path
        output_file = BASE_DIR / f"media/{unique_filename}"
        await bot.download_file(file_path, output_file)
        photo_to_delete = output_file
    elif isinstance(photo, list):
        file_info = await bot.get_file(photo[-1].file_id)
        file_extension = file_info.file_path.split(".")[-1]
        unique_filename = str(uuid.uuid4()) + "." + file_extension
        output_file = BASE_DIR / f"media/{unique_filename}"
        await photo[-1].download(destination_file=output_file)
        photo_to_delete = output_file
    params = {"worker": WORKER_ID, "amount": str(amount), "type": "deposit"}
    new_lead_status = False
    new_lead_data = {}

    with open(output_file, "rb") as file:
        new_lead_response = requests.post(
            SERVER_URL + f"/worker/requests/", params=params, files={"receipt": file}
        )
        if new_lead_response.status_code == 200:
            new_lead_status = True
            new_lead_data = new_lead_response.json()

    await message.delete()
    SUCCESS_MESSAGE = "Вы успешно отправили чек! Ожидайте подтверждение оплаты..."
    await state.finish()
    new_message = await bot.edit_message_caption(
        chat_id=message.from_user.id,
        caption=SUCCESS_MESSAGE,
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="В главное меню",
                callback_data=f"menu_order_training#{last_message_id.get('worker')}",
            )
        ),
        message_id=last_message_id.get("last_message_id"),
    )
    await bot.send_photo(
        chat_id=CHANNEL_ID,
        caption=f"<b>Новая заявка на покупку обучения Таро</b>\n\nРаботник: @{new_lead_data.get('worker').get('username')}\nСумма: {new_lead_data.get('amount')}₽",
        photo=types.InputFile(output_file),
        reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton(
                text="Подвердить ✅",
                callback_data=f"training_request_confirm#{new_lead_data.get('id')}#{new_message.message_id}#{message.from_user.id}",
            ),
            types.InlineKeyboardButton(
                text="Отклонить ❌",
                callback_data=f"training_request_decline#{new_lead_data.get('id')}#{new_message.message_id}#{message.from_user.id}",
            ),
        ),
    )

    os.remove(photo_to_delete)


@dp.callback_query_handler(inline.training_cd.filter())
async def training_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    worker = callback_data.get("worker")

    levels = {"0": start, "1": get_or_buy_course}

    current_level_function = levels[level]

    await current_level_function(callback, worker=worker)
