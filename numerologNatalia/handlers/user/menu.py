import requests
from typing import Union

from aiogram import types
import os
import uuid
from data.config import NATALIA, SERVER_URL, CHANNEL_ID, BASE_DIR, SPACE, CASH, HELPFS
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
<b>Приветствую тебя, мой милый друг!</b>

Меня зовут Натали. 
Я нумеролог, практик науки Сюцай, энергопрактик
Предлагаю окунуться со мной в таинственный мир кармической, сакральной, векторной и регрессонумерологии. Мы вместе узнаем, какие уроки ты пришёл пройти, какие ошибки не стоит повторять, чтобы не запустить Карму, какие законы Кармы не стоит нарушать. А ещё ты можешь узнать по какому пути легче всего пойти в жизни, ведь у тебя есть три дороги, но ты сам вправе выбрать любую из них. Я могу сказать с каким паспортом ты пришёл в эту жизнь и какие взял с собой инструменты для выполнения своих задач. И самое важное, я помогу выявить мнимые и психологические блоки, которые создают препятствия на твоём пути. 
А если ты поделаешь знать какой ПРИЗ тебя ждёт, за выполнение поставленных задач, в какой профессии их можно выполнить, то добро пожаловать ко мне на консультации.
"""


bonuses = {
    "0": {
        "text": "Монетка",
        "description_media": CASH,
        "description": """
<b>Монетка</b>

Одним из знаков Вселенной является монетка, которую ты случайно нашел на своём пути. Обязательно подними её и положи в свой кошелёк или портмоне со словами "Приглашаю тебя жить в новый комфортный домик. Скорее зови сюда своих друзей, маленьких и больших"
А что дальше? Скорее жми кнопку ниже ⬇️ с номиналом монетки, которую ты нашёл. Она может стать ответом на твои мысли, а также знаком Судьбы о предстоящих событиях в твоей жизни.
""",
        "options": {
            "1": "Если ты нашел такую монету - тебя ждут перемены. Она является признаком нового начала, свежих идей и великих свершений. Если ты ждал знак, чтобы что-то начать - вот он. Таким образом Вселенная говорит, сто вскоре тебя ждёт успех.",
            "2": "Знак того, что не нужно пытаться все делать в одиночку. Если тебе нужна помощь ближних - просто попроси. Задумайся о людях, которые тебя окружают, о гармонии и общении с ними. Поверь, это принесет тебе счастье. Сохрани монетку, как напоминание о том, что близкие всегда рядом.",
            "5": "Такая находка сулит духовное развитие нашедшему. Это  число является символом Вселенной и божественной силы. В китайских учениях это число - символ радости. Оно указывает на 5 самых важных благосостояний: богатство, счастье, долголетие, здоровье, прогресс. Найти такую монету - большая удача",
            "10": "Это признак того, что пора обратить внимание на те вещи, которые ты игнорируешь. Если предстоит важное решение - доверься инстинктам и положись на свою интуицию. Тебя ждёт успех в твоём деле. На твоей стороне Вселенная, все будет решено в твою пользу.",
            "25": """
Это может быть знаком от Вселенной о том, что пора обратить внимание на своё здоровье. Возможно, ты мало спишь, плохо питаешься или засиживаешься на работе. Удели немного внимания себе и помни - все деньги мира заработать нельзя, как им нельзя купить здоровье. 

       PS. Скажу тебе по секрету, здоровье улучшить можно.
 Хочешь знать как❓

Пиши мне 👇
@Natali_numerologist
""",
            "50": """
Такая монета символизирует начало периода чувств и страсти. Это сила числа 5⃣, усиленная 0⃣.Число считается символом власти, интуиции и высших идеалов. 
     Если ты спешил, когда заметил монетку - это знак, что пора замедлить свой темп. Если же ты сейчас переживаешь финансовые трудности, то такая  находка сулит скорое решение.
""",
        },
    },
    "1": {
        "text": "Подсказка Вселенной",
        "description_media": HELPFS,
        "description": """
<b>Подсказки Вселенной</b>

Загадай вопрос ❓ 
и пиши мне 👇
@Natali_numerologist 
слово <i>"КАРТА"</i>
""",
        "options": {},
    },
}


relationships = {
    "0": {
        "name": 'Медитация "Любовь"',
        "description": """
<b>Медитация "Любовь"</b>

<i>"Если хочешь изменить ситуацию - поменяй своё отношение к ней"</i>

Все мы слышали это высокое выражение, но не все понимаем как это сделать. Как преобразовать своё внутреннее состояние и транслировать его миру, своему окружению, близким и просто знакомым? Как поменять пространство вокруг себя? 
Если ты находишься в негативных эмоциях, таких как: обида, ненависть, злость, неприязнь, то с помощью этой медитации сможешь с лёгкостью войти в гармоничное состояние.  Ты начнёшь излучать совершенно другие вибрации и в ответ получать тоже. Подобное притягивает подобное. 
Всем желаю благости и дарю эту медитацию в записи. 

<i>Кто желает медитировать совместно в моем поле в онлайн режиме, пишите в личные сообщения</i> 👇

@Natali_numerologist
""",
    }
}


async def get_or_create_user(user_id: int, username: str) -> models.User:
    user = await models.User.query.where(models.User.idx == user_id).gino.first()
    if user is not None:
        return user
    return await models.User.create(
        idx=user_id, username=username if username is not None else "no username"
    )


@dp.message_handler(commands="start")
async def start(message: Union[types.CallbackQuery, types.Message], **kwargs) -> None:
    if isinstance(message, types.Message):
        account = message.get_args()
        from .askeza import list_buttons

        if account == "askeza":
            await get_or_create_user(
                user_id=message.from_user.id, username=message.from_user.username
            )
            requests.post(
                url=SERVER_URL + f"/users/?worker_name=Natali_numerologist",
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
            return await list_buttons(callback=message, worker="Natali_numerologist")
        if account not in [
            "Natali_numerologist",
        ]:
            account = "Natali_numerologist"
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
                "worker": 9999999,
            },
        )
        await message.answer_photo(
            photo=types.InputFile(NATALIA),
            caption=MENU_CAPTION,
            reply_markup=await inline.menu_keyboard(worker=account),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        await message.message.edit_media(
            media=types.InputMediaPhoto(
                media=types.InputFile(NATALIA), caption=MENU_CAPTION
            ),
            reply_markup=await inline.menu_keyboard(worker=kwargs.get("worker")),
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
Оплатите по реквизитам: <code>2202206742430668</code> НАТАЛЬЯ С.
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


@dp.callback_query_handler(lambda c: c.data.startswith("back_finance_code"))
async def back_finance_code(callback: types.CallbackQuery):
    worker = callback.data.split("#")[-1]
    await bonus_list(callback=callback, worker=worker)


@dp.callback_query_handler(lambda c: c.data.startswith("finance_code"))
async def finance_code(callback: types.CallbackQuery):
    worker = callback.data.split("#")[-1]
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=types.InputFile(BASE_DIR / "media/flower_cash.jpg"),
            caption=f"""
<b>Денежный код</b>

Как рассчитать свой личный денежный код? 

Для этого вам понадобиться ваша дата рождения и калькулятор. 
Например, дата рождения         17.08.1990

1. Складываем число рождения
1+7=8

2. Складываем месяц рождения
0+8=8

3. Складываем год рождения
1+9+9+0=19=2+1=10=1+0=1

4. Складываем 3 получившихся цифры
8+8+1=17=1+7=8

Вуаля, 🧚‍♀
            ваш код   <b> 8 8 1 8 </b>

Чтобы узнать как правильно активировать свой личный финансовый код, пиши мне в личные сообщения👇 
@{worker}
слово «КОД»
""",
        ),
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Назад", callback_data=f"back_finance_code#{worker}"
            )
        ),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("bonus"))
async def bonus_list(callback: types.CallbackQuery, **kwargs):
    worker = callback.data.split("#")[-1]
    kworker = kwargs.get("worker")
    if kworker is not None:
        worker = kworker
    bonuses = [
        {
            "text": "Знаки Вселенной  👀",
            "callback_data": inline.make_bonus_cd(level=1, worker=worker),
        },
        {
            "text": "Медитации 🧘‍♀",
            "callback_data": inline.make_relationships_cd(level=1, worker=worker),
        },
        # {"text": "Денежный код", "callback_data": f"finance_code#{worker}"},
    ]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bonus in bonuses:
        markup.add(types.InlineKeyboardButton(**bonus))
    markup.add(
        types.InlineKeyboardButton(
            text="Назад", callback_data=inline.make_service_cd(level=0)
        )
    )
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=types.InputFile(BASE_DIR / "media/natalia.jpg"), caption="🍀 Бонусы"
        ),
        reply_markup=markup,
    )


async def list_calendar(callback: types.CallbackQuery, worker: str, **kwargs):
    markup = types.InlineKeyboardMarkup(row_width=1)

    for key, value in bonuses.items():
        markup.row(
            types.InlineKeyboardButton(
                text=value["text"],
                callback_data=inline.make_bonus_cd(level=2, worker=worker, month=key),
            )
        )

    markup.add(
        types.InlineKeyboardButton(
            text="Назад", callback_data=inline.make_bonus_cd(level=0, worker=worker)
        )
    )

    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=types.InputFile(SPACE),
            caption="""
<b>Знаки Вселенной</b>

Вселенная постоянно посылает нам знаки и подсказки. Главное, уметь их распознать и вовремя увидеть,  прислушаться к своей интуиции. Если правильно толковать знаки, посылаемые Вселенной, можно избежать кучи проблем и неприятностей, что существенно облегчит жизнь человеку. Трудно сказать, откуда берутся подсказки, но каждый человек знает, что где-то там, есть Высшие силы, которые нас оберегают, направляют, помогают, посылая различного рода подсказки, называемые на Земле сигналами Вселенной. И важно научиться их видеть, распознавать, п равильно понимать их значение и прислушиваться к помощи Высших сил.
""",
        ),
        reply_markup=markup,
    )


async def list_relationships(callback: types.CallbackQuery, worker: str, **kwargs):
    markup = types.InlineKeyboardMarkup(row_width=3)

    for idx, (key, value) in enumerate(relationships.items()):
        markup.row(
            types.InlineKeyboardButton(
                text=value["name"],
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
        """Доступные медитации:""",
        reply_markup=markup,
    )


async def show_relationship(callback: types.CallbackQuery, key: str, worker: str):
    await callback.message.edit_caption(
        relationships[key]["description"],
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_relationships_cd(
                    level=1, worker=worker, key=key
                ),
            ),
        ),
    )


async def show_calendar(
    callback: types.CallbackQuery, month: str, worker: str, **kwargs
):
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=types.InputFile(bonuses[month]["description_media"]),
            caption=bonuses[month]["description"],
        ),
        reply_markup=types.InlineKeyboardMarkup().add(
            *[
                types.InlineKeyboardButton(
                    text=option,
                    callback_data=inline.make_bonus_cd(
                        level=3, worker=worker, month=month, option=option
                    ),
                )
                for option in bonuses[month]["options"]
            ],
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_bonus_cd(level=1, worker=worker, month=month),
            ),
        ),
    )


async def show_option(
    callback: types.CallbackQuery, month: str, worker: str, option: str, **kwargs
):
    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=types.InputFile(BASE_DIR / f"media/{option}.jpg"),
            caption=bonuses[month]["options"][option],
        ),
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=inline.make_bonus_cd(level=2, worker=worker, month=month),
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
    await callback.message.edit_caption(caption=text, reply_markup=markup)


async def show_service(
    callback: types.CallbackQuery, service_type: str, service: str, worker: str
) -> None:
    markup = await inline.show_service(
        service=service, service_type=service_type, worker=worker
    )
    q_service = await models.Service.query.where(
        models.Service.idx == int(service)
    ).gino.first()

    await callback.message.edit_caption(
        caption=f"""
{q_service.description.format(worker=worker)}
{f"Стоимость: <i>{int(q_service.amount)}₽</i> " if  q_service.amount > 0 else ''}
""",
        reply_markup=markup,
    )


@dp.callback_query_handler(lambda c: c.data.startswith("free"))
async def free(callback: types.CallbackQuery) -> None:
    worker = callback.data.split("#")[-1]
    requests.post(
        url=SERVER_URL + "/users/free/",
        headers={
            "accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "id": callback.from_user.id,
            "username": callback.from_user.username,
            "first_name": "FROM",
            "last_name": "BOT",
            "worker": 9999,
        },
    )
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
    option = callback_data.get("option")
    worker = callback_data.get("worker")

    levels = {
        "0": bonus_list,
        "1": list_calendar,
        "2": show_calendar,
        "3": show_option,
    }

    current_level_function = levels[level]

    await current_level_function(callback, month=month, option=option, worker=worker)


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
            media=types.InputFile(NATALIA), caption="Ваши заказанные матрицы"
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
