import requests
from typing import Union

from aiogram import types
import os
import uuid
from data.config import VIKTORIA, SERVER_URL, CHANNEL_ID, BASE_DIR
from math import ceil
from database import models
from keyboards.user import inline
from aiogram.dispatcher import FSMContext
from filters.is_connected import IsConnected
from states.matrix import Matrix
from states.matrix_buy import MatrixBuy
from io import BytesIO
from loader import dp, bot

MENU_CAPTION = """
<b>Приветствую Вас!</b>😌
Меня зовут Виктория. Я практикующий нумеролог.
Консультирую и обучаю. 

💫На моем счету более 1000 успешных консультаций.

С помощью своих знаний я могу продиагностировать Вашу проблему и подобрать для Вас оптимальную консультацию или практику, нацеленную на ваши запросы по определённой сфере жизни.
И я, как никто знаю, что у каждого из нас есть возможность изменить свою жизнь к лучшему, благодаря той силе, что скрыта внутри нас! 
‌Я помогаю скорректировать Ваши жизненные пути, раскрыть Ваш внутренний потенциал и улучшить финансовое положение. 
‌
‌Умею составлять подробный прогноз на ближайший год/месяц. Располагаю новейшими методиками Ставов, направленных на расширение основных сфер жизни, которые дают прекрасный результат!
"""


calendar_haircut = {
    "Июнь": """
Самые благоприятные дни для стрижки волос в июне ✂️ 

✅ - Благоприятные дни - 24, 25, 27  июня

❌ - Неблагоприятные - 26 июня 

Остальные - нейтральные
""",
    "Июль": """
Самые благоприятные дни для стрижки волос в июле ✂️ 

✅ - Благоприятные дни - 12, 18, 19, 20, 21, 22, 23, 24, 30 

❌ - Неблагоприятные - 3, 4, 5, 6, 7, 8, 9, 10, 16, 17, 25 

Остальные - нейтральные
""",
    "Август": """
Самые благоприятные дни для стрижки волос в Августе 2023 г. ✂️ 

✅ - Благоприятные дни - 7, 8, 14, 15, 17, 18, 19, 20, 21, 27, 28. 

❌ - Неблагоприятные - 1, 2, 3, 4, 5, 6, 12, 13, 24, 25, 31 

Остальные - нейтральные
""",
    "Сентябрь": """
Самые благоприятные дни для стрижки волос в Сентябре 2023г. ✂️ 

✅ - Благоприятные дни - 4, 5, 11, 12, 13, 14, 16, 17, 24, 

❌ - Неблагоприятные - 1, 2, 3, 8, 9, 10, 27, 28, 29, 30. 

Остальные - нейтральные
""",
    "Октябрь": """
Самые благоприятные дни для стрижки волос в Октябре 2023 г. ✂️ 

✅ - Благоприятные дни - 1, 2, 8, 9, 10, 11, 12, 20, 21, 28. 

❌ - Неблагоприятные - 6, 7, 13, 14, 23, 24, 25, 26, 27. 

Остальные - нейтральные
""",
    "Ноябрь": """
Самые благоприятные дни для стрижки волос в Ноябре 2023 г. ✂️ 

✅ - Благоприятные дни - 4, 5, 6, 7, 8, 16, 17, 25, 26, 27

❌ - Неблагоприятные - 2, 3, 12, 13, 21, 22, 23, 24, 28, 29, 30

Остальные - нейтральные
""",
    "Декабрь": """
Самые благоприятные дни для стрижки волос в Декабре 2023 г. ✂️ 

✅ - Благоприятные дни - 2, 3, 4, 5, 6, 14, 15, 22, 23, 24, 25, 29, 30, 31

❌ - Неблагоприятные - 1, 9, 10, 11, 12, 13, 18, 19, 20, 21, 27, 28. 

Остальные - нейтральные
""",
}


relationships = {
    "0": """
В вашей паре  очень много проработок и обнулений в течение жизни.
Полученное число свидетельствует о том, что у вашей пары нет совместного будущего.

Это не говорит, что вы не можете быть вместе, просто многие не выдерживают такое количество испытаний, но все в ваших руках, придется потрудиться 🤷🏼‍♀️

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "1": """
🤔 Однажды вам уже приходилось встречаться в прошлом, и ваша любовь была сильной. Однако в этой жизни связь между вами вряд ли приведет к хорошему результату. 

☝🏻Но, помните, что это только кармический показатель который дает доп.проработки, а так все только в ваших руках.

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "2": """
🤔 Однажды вам уже приходилось встречаться в прошлом, и ваша любовь была сильной. Однако в этой жизни связь между вами вряд ли приведет к хорошему результату. 

☝🏻Но, помните, что это только кармический показатель который дает доп.проработки, а так все только в ваших руках.

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "3": """
😳 В таком союзе главной является женщина. Если мужчина сможет это принять, то отношения могут продлиться долго. 

Но, еще зависит от характера. Это только кармический показатель который дает доп.проработки и все не так гладко.

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "4": """
Супер 🙌🏼 
Ничего страшного. Кармическая связь в таких отношениях есть, но она очень слабая. Поэтому особо ничего не угрожает.

Как минимум по этому показателю проработок нет 👍🏼

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "5": """
Да уж 😁
Скучно точно не будет. Сильная духовная и кармическая связь, из-за которой людей тянет друг к другу. 🧲 
Такие отношения могут просуществовать очень долго.

Очень интересная связь. 

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "6": """
😳😳😳 Опасное число. Оно означает, что в прошлом вы были очень близки, но кто-то погиб рано, что заставило другого страдать. Отношения могут быть долгими и мучительными.

Но, не пугайтесь, это только кармический показатель, в ваших руках выстроить отношения которые вас вполне устраивают, но не без проработок 🤷🏼‍♀️

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "7": """
Отлично. 👍🏼 
Удачный союз 😍😍😍

Число семь сулит долгую и счастливую совместную жизнь. 
Как минимум по этому показателю у вас все прекрасно 🙌🏼

Вполне можно выстроить хорошие отношения. 

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "8": """
Уууу...В нумерологии это число считается символом бесконечности. ♾️♾️♾️

Оно говорит о том, что вы встречались в прошлой жизни 😳 и еще не раз встретитесь в будущем.

Проработочки есть, не просто так вы встретились. Помним о том, что это только кармический показатель, все можно выстроить так как вы хотите 🤗

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
    "9": """
Поздравляю.🙌🏼🙌🏼🙌🏼

Кармическая связь отсутствует, поэтому длительность отношений зависит только от вас самих 😍

Вам повезло, кармических проработок по этому показателю нет 🙌🏼

На полный разбор по совместимости можно записаться по кнопке ниже ⬇️
""",
}


async def get_or_create_user(user_id: int, username: str) -> models.User:
    user = await models.User.query.where(models.User.idx == user_id).gino.first()
    if user is not None:
        await models.User.update.values(is_active=True).where(
                models.User.idx == user.idx
            ).gino.status()
        return user
    return await models.User.create(
        idx=user_id, username=username if username is not None else "no username"
    )


async def proceed_signin(message):
    await get_or_create_user(
                user_id=message.from_user.id, username=message.from_user.username
            )
    requests.post(
        url=SERVER_URL + f"/users/?worker_name=viktoria_numer",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "worker": 9999,
        },
    )

@dp.message_handler(commands="start")
async def start(message: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    from . import askeza, numercourse, forecastcourse
    if isinstance(message, types.Message):
        account = message.get_args()
        try:
            services = {
                "fincode": "6️⃣ Финансовый код",
                "moncharm": "5️⃣ Став денежный амулет",
                "energy": "9️⃣ Энергетическая отвязка",
                "monform": "🔟 Денежная нейроформула",
                "helsaf": "7️⃣ Став «Помощь»",
                "onetwomon": "3️⃣ Прогноз на 1-2 месяца",
                "fullprog": "4️⃣ Подробный прогноз на год"
            }
            # service_idx = int(account)
            is_service = await models.Service.query.where(models.Service.name == services[account]).gino.first()
            if is_service is not None:
                await proceed_signin(message=message)
                return await show_service(callback=message, service_type="1", service=is_service.idx, worker="viktoria_numer")
        except (ValueError, KeyError):
            pass
        if account == "askeza":
            await proceed_signin(message=message)
            return await askeza.list_buttons(callback=message, worker="viktoria_numer")
        if account == "services":
            await proceed_signin(message=message)
            return await list_services(callback=message, service_type="1", worker="viktoria_numer")
        if account == "timeoclock":
            from .timeoclock import list_buttons
            await proceed_signin(message=message)
            return await list_buttons(callback=message, worker="viktoria_numer")
        if account == "taro":
            from .training import list_courses
            await proceed_signin(message=message)
            return await list_courses(callback=message, worker="viktoria_numer")
        if account == "course_numerology":
            await proceed_signin(message=message)
            return await numercourse.list_buttons(callback=message, worker="viktoria_numer")
        if account == "course_prognoz":
            await proceed_signin(message=message)
            return await forecastcourse.list_buttons(callback=message, worker="viktoria_numer")
        if account == "free":
            await proceed_signin(message=message)
            return await free(callback=message, worker="viktoria_numer")
        if account == "2024":
            await proceed_signin(message=message)
            return await s2024(callback=message, worker="viktoria_numer")
        if account not in ["viktoria_numer", "numerolog_viktoriia"]:
            account = "viktoria_numer"
        await get_or_create_user(
            user_id=message.from_user.id, username=message.from_user.username
        )
        requests.post(
            url=SERVER_URL + f"/users/?worker_name={account}",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "id": message.from_user.id,
                "username": message.from_user.username,
                "first_name": "FROM",
                "last_name": "BOT",
                "worker": 9999,
            },
        )
        await message.answer_photo(
            photo=types.InputFile(VIKTORIA),
            caption=MENU_CAPTION,
            reply_markup=await inline.menu_keyboard(worker=account),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        await message.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(VIKTORIA), caption=MENU_CAPTION
            ),
            reply_markup=await inline.menu_keyboard(worker=kwargs.get("worker")),
        )

@dp.callback_query_handler(lambda c: c.data.startswith("s2024"))
async def s2024(callback: Union[types.CallbackQuery, types.Message], worker: str = "viktoria_numer") -> None:
    if isinstance(callback, types.CallbackQuery):
        worker = callback.data.split("#")[-1]
        await callback.message.edit_caption(
        caption=f"""

Вы узнаете какая главная задача у вас на 2024 год. 
Напишите мне 👇🏻

@{worker}

«Прогноз 2024» и я скину всю информацию.

""",
        reply_markup=await inline.free_markup(worker=worker),
    )
    elif isinstance(callback, types.Message):
        await callback.answer_photo(
            photo=types.InputFile(VIKTORIA),
        caption=f"""

Вы узнаете какая главная задача у вас на 2024 год. 
Напишите мне 👇🏻

@{worker}

«Прогноз 2024» и я скину всю информацию.

""",
        reply_markup=await inline.free_markup(worker=worker),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("order_matrix"))
async def order_matrix(callback: types.CallbackQuery, state: FSMContext):
    worker = callback.data.split("#")[-1]
    new_message = await callback.message.edit_caption(
        "Введите свою дату рождения в формате: 01.01.2000",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(text="Назад", callback_data="order_matrix_back")
        ),
    )
    await Matrix.dob.set()
    await state.set_data({"last_message_id": new_message.message_id, "worker": worker})


@dp.callback_query_handler(lambda c: c.data == "order_matrix_back", state=Matrix.dob)
async def order_matrix_back(callback: types.CallbackQuery, state: FSMContext):
    cdata = await state.get_data()
    worker = cdata.get("worker")
    await state.finish()
    await start(message=callback, worker=worker)


@dp.callback_query_handler(lambda c: c.data.startswith("menu_order_matrix"))
async def order_matrix_menu(callback: types.CallbackQuery):
    worker = callback.data.split("#")[-1]
    await start(message=callback, worker=worker)


@dp.callback_query_handler(
    lambda c: c.data.startswith("menu_order_matrix"), state=MatrixBuy.receipt
)
async def order_matrix_cancel(callback: types.CallbackQuery, state: FSMContext):
    worker = callback.data.split("#")[-1]
    await state.finish()
    await start(message=callback, worker=worker)


@dp.message_handler(regexp=r"\d{2}.\d{2}.\d{4}", state=Matrix.dob)
async def order_matrix_dob(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        last_message_id = data["last_message_id"]
        dob = message.text
        await message.delete()
        new_message = await bot.edit_message_caption(
            chat_id=message.from_user.id,
            caption=f"Ваша дата рождения: {dob} указана правильно?\n\n<b>Просто введите другую, если хотите изменить...</b>",
            reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
                types.InlineKeyboardButton(
                    text="да", callback_data=f"order_matrix_confirm#{dob}"
                ),
                types.InlineKeyboardButton(
                    text="Отмена", callback_data="order_matrix_back"
                ),
            ),
            message_id=last_message_id,
        )
        data["last_message_id"] = new_message.message_id


@dp.callback_query_handler(
    lambda c: c.data.startswith("order_matrix_confirm"), state=Matrix.dob
)
async def order_matrix_confirm(callback: types.CallbackQuery, state: FSMContext):
    dob = callback.data.split("#")[-1]
    cdata = await state.get_data("worker")
    worker = cdata.get("worker")
    await state.finish()
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\nСоединяемся со Вселенной, подождите...."
    )
    response = requests.post(
        SERVER_URL + "/matrix/requests/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "user": callback.from_user.id,
            "dob": dob,
        },
    )
    data = response.json()
    image = requests.get(SERVER_URL.replace("/api/v1", "/") + data.get("image"))

    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            types.InputFile(BytesIO(image.content)),
            caption=data.get("result")[:256]
            + "..."
            + "\n\n<b>Чтобы узнать подробнее, оплатите отчёт</b>",
        ),
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Оплатить",
                callback_data=f"buy_matrix#{data.get('id')}#{worker}",
            ),
            types.InlineKeyboardButton(
                text="Отмена", callback_data=f"menu_order_matrix#{worker}"
            ),
        ),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("deposit_request_confirm"))
async def deposit_request_confirm(callback: types.CallbackQuery):
    mrequest_id = int(callback.data.split("#")[1])
    wrequest_id = int(callback.data.split("#")[2])
    last_message_id = int(callback.data.split("#")[3])
    user_id = int(callback.data.split("#")[4])
    worker = callback.data.split("#")[5]

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
    response = requests.get(SERVER_URL + f"/matrix/requests/{mrequest_id}")
    matrix = response.json()
    result = matrix.get("result")
    page_size = 1024
    max_pages = ceil(len(result) / page_size)
    await bot.edit_message_caption(
        chat_id=user_id,
        caption=result[0:1024],
        reply_markup=await inline.show_matrix(
            worker=worker,
            matrix_page=1,
            request_id=matrix.get("id"),
            page=1,
            max_pages=max_pages,
        ),
        message_id=last_message_id,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("deposit_request_decline"))
async def deposit_request_decline(callback: types.CallbackQuery):
    mrequest_id = int(callback.data.split("#")[1])
    wrequest_id = int(callback.data.split("#")[2])
    last_message_id = int(callback.data.split("#")[3])
    user_id = int(callback.data.split("#")[4])
    worker = callback.data.split("#")[5]

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
        caption="Ваша заявка на покупку матрицы отклонена",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Назад", callback_data=f"menu_order_matrix#{worker}"
            )
        ),
        message_id=last_message_id,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("buy_matrix"))
async def buy_matrix(callback: types.CallbackQuery):
    mid = callback.data.split("#")[1]
    worker = callback.data.split("#")[2]
    await callback.message.edit_caption(
        caption="""
Оплатите по реквизитам: <code>4276673835364343</code>

<b>Получатель:</b> Сергей Андреевич К.
<b>Банк:</b> Сбербанк.

Сумма: <code>500</code>₽

После оплаты нажмите кнопку <b>Подтвердить</b> и прикрепите чек в формате скриншота.
""",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Подтвердить", callback_data=f"confirm_buy_matrix#{mid}#{worker}"
            ),
            types.InlineKeyboardButton(
                text="Отмена", callback_data=f"menu_order_matrix#{worker}"
            ),
        ),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("confirm_buy_matrix"))
async def buy_matrix_confirm(callback: types.CallbackQuery, state: FSMContext):
    mid = callback.data.split("#")[1]
    worker = callback.data.split("#")[2]
    new_message = await callback.message.edit_caption(
        "Отправьте чек в формате скриншота",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отмена", callback_data=f"menu_order_matrix#{worker}"
            )
        ),
    )
    await MatrixBuy.receipt.set()
    await state.set_data(
        {"mid": mid, "last_message_id": new_message.message_id, "worker": worker}
    )


@dp.message_handler(
    content_types=[types.ContentType.DOCUMENT, types.ContentType.PHOTO],
    state=MatrixBuy.receipt,
)
async def control_amount(message: types.Message, state: FSMContext) -> None:
    amount = 500
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
    params = {"worker": 5625107813, "amount": str(amount), "type": "deposit"}
    new_lead_status = False
    new_lead_data = {}

    with open(output_file, "rb") as file:
        new_lead_response = requests.post(
            SERVER_URL + f"/worker/requests/", params=params, files={"receipt": file}
        )
        if new_lead_response.status_code == 200:
            new_lead_status = True
            new_lead_data = new_lead_response.json()

    requests.patch(
        SERVER_URL + f"/matrix/requests/{last_message_id.get('mid')}/",
        params={
            "worker_request": new_lead_data.get("id"),
        },
        headers={
            "accept": "application/json",
        },
    )
    await message.delete()
    SUCCESS_MESSAGE = "Вы успешно отправили чек! Ожидайте подтверждение оплаты..."
    await state.finish()
    new_message = await bot.edit_message_caption(
        chat_id=message.from_user.id,
        caption=SUCCESS_MESSAGE,
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="В главное меню",
                callback_data=f"menu_order_matrix#{last_message_id.get('worker')}",
            )
        ),
        message_id=last_message_id.get("last_message_id"),
    )

    await bot.send_photo(
        chat_id=CHANNEL_ID,
        caption=f"<b>Новая заявка на покупку матрицы</b>\n\nРаботник: @{new_lead_data.get('worker').get('username')}\nСумма: {new_lead_data.get('amount')}₽",
        photo=types.InputFile(output_file),
        reply_markup=await inline.confirm_deposit_request_keyboard(
            last_message_id.get("mid"),
            new_lead_data.get("id"),
            new_message.message_id,
            message.from_user.id,
            worker=last_message_id.get("worker"),
        ),
    )

    os.remove(photo_to_delete)


@dp.callback_query_handler(lambda c: c.data.startswith("bonus"))
async def bonus_list(callback: types.CallbackQuery, **kwargs):
    worker = callback.data.split("#")[-1]
    kworker = kwargs.get("worker")
    if kworker is not None:
        worker = kworker
    bonuses = [
        {
            "text": "Календарь стрижек",
            "callback_data": inline.make_bonus_cd(level=1, worker=worker),
        },
        {
            "text": "Кармическая совместимость",
            "callback_data": inline.make_relationships_cd(level=1, worker=worker),
        },
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bonus in bonuses:
        markup.add(types.InlineKeyboardButton(**bonus))
    markup.add(
        types.InlineKeyboardButton(
            text="Назад", callback_data=inline.make_service_cd(level=0)
        )
    )
    await callback.message.edit_caption("Бонусы🎁", reply_markup=markup)


async def list_calendar(callback: types.CallbackQuery, worker: str, **kwargs):
    markup = types.InlineKeyboardMarkup(row_width=1)

    for date in calendar_haircut:
        markup.row(
            types.InlineKeyboardButton(
                text=date,
                callback_data=inline.make_bonus_cd(level=2, worker=worker, month=date),
            )
        )

    markup.add(
        types.InlineKeyboardButton(
            text="Назад", callback_data=inline.make_bonus_cd(level=0, worker=worker)
        )
    )

    await callback.message.edit_caption("📅Календарь стрижек", reply_markup=markup)


async def list_relationships(callback: types.CallbackQuery, worker: str, **kwargs):
    markup = types.InlineKeyboardMarkup(row_width=3)

    for idx, key in enumerate(relationships):
        if idx == 1:
            markup.row(
                types.InlineKeyboardButton(
                    text=key,
                    callback_data=inline.make_relationships_cd(
                        level=2, worker=worker, key=key
                    ),
                )
            )
        else:
            markup.insert(
                types.InlineKeyboardButton(
                    text=key,
                    callback_data=inline.make_relationships_cd(
                        level=2, worker=worker, key=key
                    ),
                )
            )
    markup.add(
        types.InlineKeyboardButton(
            text="Назад",
            callback_data=inline.make_relationships_cd(level=0, worker=worker),
        )
    )

    await callback.message.edit_caption(
        """
<b>Кармические ли у вас отношения?,</b> 🤔 

Этот расчет будет очень кстати, он поможет произвести анализ и понять основной вектор направленности взаимоотношений, есть ли кармическая составляющая связи, и, какая она положительная или отрицательная. 

<b>Как сделать расчет?</b>

Возьмите свою дату рождения и дату рождения вашего партнера сложите все числа. 
Пример ⬇️

05.01.1995 и 23.01.1993
Складываем ваши даты: 

5+1+1+9+9+5+2+3+1+1+9+9+3=58

Получилось число 58. Вы берете последнюю цифру т.е ваше число 8 именно оно и является кармическим числом отношений вашей пары. 

Смотрим значение вашего числа. ⬇️
""",
        reply_markup=markup,
    )


async def show_relationship(callback: types.CallbackQuery, key: str, worker: str):
    await callback.message.edit_caption(
        relationships[key],
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Записаться на разбор",
                url="https://api.whatsapp.com/send/?phone=79292084866&text=Привет!+Хочу+разбор+по+совместимости+за+2000₽&type=phone_number&app_absent=0?",
            ),
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_relationships_cd(
                    level=1, worker=worker, key=key
                ),
            ),
        ),
    )


async def show_calendar(callback: types.CallbackQuery, month: str, worker: str):
    await callback.message.edit_caption(
        calendar_haircut[month],
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_bonus_cd(level=1, worker=worker, month=month),
            )
        ),
    )


async def list_service_types(callback: types.CallbackQuery, worker, **kwargs) -> None:
    markup = await inline.service_types_keyboard(worker=worker)
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"
    await callback.message.edit_caption(caption=text, reply_markup=markup)


async def list_services(
    callback: types.CallbackQuery, service_type: str, worker: str, **kwargs
) -> None:
    markup = await inline.services_keyboard(service_type, worker)
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"
    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_caption(caption=text, reply_markup=markup)
    elif isinstance(callback, types.Message):
        await callback.answer_photo(photo=types.InputFile(VIKTORIA), caption=text, reply_markup=markup)


async def show_service(
    callback: Union[types.CallbackQuery, types.Message], service_type: str, service: str, worker: str
) -> None:
    markup = await inline.show_service(
        service=service, service_type=service_type, worker=worker
    )
    q_service = await models.Service.query.where(
        models.Service.idx == int(service)
    ).gino.first()

    if isinstance(callback, types.CallbackQuery):
        await callback.message.edit_caption(
        caption=f"""
{q_service.description.format(worker=worker)}
{f"Стоимость: <i>{int(q_service.amount)}₽</i> " if  q_service.amount > 0 else ''}
""",
        reply_markup=markup,
    )
    elif isinstance(callback, types.Message):
     await callback.answer_photo(
         photo=types.InputFile(VIKTORIA),
        caption=f"""
{q_service.description.format(worker=worker)}
{f"Стоимость: <i>{int(q_service.amount)}₽</i> " if  q_service.amount > 0 else ''}
""",
        reply_markup=markup,
    )   


@dp.callback_query_handler(lambda c: c.data.startswith("free"))
async def free(callback: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    requests.post(
        url=SERVER_URL + "/users/free/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": callback.from_user.id,
            "username": callback.from_user.username,
            "first_name": callback.from_user.first_name,
            "last_name": callback.from_user.last_name,
            "worker": 9999,
        },
    )
    if isinstance(callback, types.Message):
        worker = kwargs.get("worker")
        await callback.answer_photo(
        photo=types.InputFile(VIKTORIA),
        caption=f"""
Отправьте дату своего рождения мне в личном сообщении 
<b>НАЖАТЬ</b> 👉🏻  @{worker}

Пример: 12.09.1978
""",
        reply_markup=await inline.free_markup(worker=worker),
    )
    elif isinstance(callback, types.CallbackQuery):
        worker = callback.data.split("#")[-1]
        await callback.message.edit_caption(
            caption=f"""
Отправьте дату своего рождения мне в личном сообщении 
<b>НАЖАТЬ</b> 👉🏻  @{worker}

Пример: 12.09.1978
""",
            reply_markup=await inline.free_markup(worker=worker),
        )


@dp.callback_query_handler(inline.bonus_cd.filter())
async def bonus_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    month = callback_data.get("month")
    worker = callback_data.get("worker")

    levels = {
        "0": bonus_list,
        "1": list_calendar,
        "2": show_calendar,
    }

    current_level_function = levels[level]

    await current_level_function(callback, month=month, worker=worker)


@dp.callback_query_handler(inline.relationships_cd.filter())
async def relationships_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    key = callback_data.get("key")
    worker = callback_data.get("worker")

    levels = {
        "0": bonus_list,
        "1": list_relationships,
        "2": show_relationship,
    }

    current_level_function = levels[level]

    await current_level_function(callback, key=key, worker=worker)


@dp.callback_query_handler(inline.service_cd.filter())
async def service_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    service_type = 1
    service = callback_data.get("service")
    worker = callback_data.get("worker")

    levels = {
        "0": start,
        # "1": list_service_types,
        "1": list_services,
        "2": show_service,
    }

    current_level_function = levels[level]

    await current_level_function(
        callback, service=service, service_type=service_type, worker=worker
    )


async def list_matrix(callback: types.CallbackQuery, worker, page, **kwargs):
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=types.InputFile(VIKTORIA),
            caption="Ваши заказанные матрицы"
        ),
        reply_markup=await inline.list_matrix(
            worker=worker, user_id=callback.from_user.id, current_page=page
        ),
    )


async def show_matrix(
    callback: types.CallbackQuery, worker, page, request_id, matrix_page
):
    response = requests.get(SERVER_URL + f"/matrix/requests/{request_id}")
    matrix = response.json()
    result = matrix.get("result")
    page_size = 1024
    start_index = (int(matrix_page) - 1) * page_size
    end_index = int(matrix_page) * page_size
    max_pages = ceil(len(result) / page_size)
    worker_request = matrix.get("worker_request")
    image = requests.get(SERVER_URL.replace("/api/v1", "/") + matrix.get("image"))
    if worker_request.get("is_success"):
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                types.InputFile(BytesIO(image.content)),
                caption=result[start_index:end_index],
            ),
            reply_markup=await inline.show_matrix(
                worker=worker,
                matrix_page=matrix_page,
                request_id=request_id,
                page=page,
                max_pages=max_pages,
            ),
        )
    else:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                types.InputFile(BytesIO(image.content)),
                caption=result[0:512],
            ),
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton(
                    text="Оплатить",
                    callback_data=f"buy_matrix#{matrix.get('id')}#{worker}",
                ),
                types.InlineKeyboardButton(
                    text="Отмена", callback_data=f"menu_order_matrix#{worker}"
                ),
            ),
        )


@dp.callback_query_handler(inline.matrix_cd.filter())
async def matrix_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    worker = callback_data.get("worker")
    page = callback_data.get("page")
    request_id = callback_data.get("request_id")
    matrix_page = callback_data.get("matrix_page")

    levels = {
        "0": start,
        "1": list_matrix,
        "2": show_matrix,
    }

    current_level_function = levels[level]

    await current_level_function(
        callback,
        page=page,
        request_id=request_id,
        worker=worker,
        matrix_page=matrix_page,
    )
