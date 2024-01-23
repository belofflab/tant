from aiogram import types

from database import models
from keyboards.admin import inline
from loader import dp, bot
from states.sender import Sender as SenderState
from utils import image, sender
from data.config import BASE_DIR, SERVER_URL
import requests
from filters.is_admin import IsAdmin
from aiogram.dispatcher import FSMContext


async def get_or_create_user(user_id: int, username: str) -> models.User:
    user = await models.User.query.where(models.User.idx == user_id).gino.first()
    if user is not None:
        return user
    return await models.User.create(
        idx=user_id, username=username if username is not None else "no username"
    )


@dp.message_handler(IsAdmin(), commands="contacts")
async def contacts(message: types.Message):
    import json

    contacts = json.loads(open(BASE_DIR / "contacts.json", "r").read())
    for contact in contacts:
        await get_or_create_user(
            user_id=contact.get("id"),
            username=contact.get("username").replace("@", "")
            if contact.get("username")
            else contact.get("username"),
        )
        requests.post(
            url=SERVER_URL
            + f"/users/date/?last_activity={contact.get('first_touch')}&first_touch={contact.get('first_touch')}",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "id": contact.get("id"),
                "username": contact.get("username").replace("@", "")
                if contact.get("username")
                else contact.get("username"),
                "first_name": contact.get("full_name"),
                "last_name": None,
                "worker": 9999,
            },
        )

    await message.answer("ok")


@dp.message_handler(IsAdmin(), commands="setup")
async def setup(message: types.Message) -> None:
    service_types = [{"idx": 1, "name": "TEST"}]

    for service_type in service_types:
        await models.ServiceType.create(**service_type)

    services = [
        {
            "name": "Один вопрос 🙋🏻‍♀️",
            "type": 1,
            "description": """
- Напишите «Хочу ответ на один вопрос» сформулируйте свой вопрос, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻
 
🙎‍♀️@{worker}
""",
            "amount": "1000",
        },
        {
            "name": "Два вопроса 🙋🏻‍♀️",
            "type": 1,
            "description": """
- Напишите «Хочу ответ на два вопроса» сформулируйте свой вопрос, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻

🙎‍♀️@{worker}
""",
            "amount": "1650",
        },
        {
            "name": "Тема 🌄",
            "type": 1,
            "description": """
Мы можем рассмотреть любой ваш запрос по определенной теме:
1. Финансы
2. Бизнез
3. Отношения
4. Духовность 
5. Поток от Высшего Я + совет
Вы составляете свои вопросы которые вас волнуют и мы выстраиваем дальше цепочку ….

Вопросы НЕ СМОТРЮ
❌Продам, не продам…
❌Куплю, не куплю…. 

Чтобы заказать услугу пиши в личные сообщения 👇
🙎‍♀️@{worker}
""",
            "amount": "2700",
        },
        {
            "name": "Диагностика чакр",
            "type": 1,
            "description": """
<b>Диагностика без чистки!</b>

Жизнь физического тела без энергетического невозможна!

<b>Функции чакр:</b> чакры поглощают, накапливают, очищают и перерабатывают энергию окружающей среды, а также энергию самого человека. 
<b>Если в жизни пошла *ОПА</b>, то нужно обратить внимание на свои энергоканалы и конечно же на окружение. 
Через таро и фото дам 
обратную связь над какими нужно работать.

Чтобы  заказать диагностику  пиши в личные сообщения 👇 
🙎‍♀️@{worker}
""",
            "amount": "2000",
        },
        {
            "name": "Чистка энергоканалов",
            "type": 1,
            "description": """
<b>Чистка и наполнение чакр</b>

Если у вас присутствует лень, усталость, апатия, гнев, нет энергии и т.д…..
То пришло время <b>чистить ваши энергоканалы </b>
Я через свои потоки сделаю очищение и наполнение. 

Что вы получите? 
Прилив энергий и сил! 
Чистка + наполнение длиться 7 дней

Чтобы заказать чистку пишите в личные сообщения 👇
🙎‍♀️@{worker}
""",
            "amount": "6300",
        },
        {
            "name": "Прогноз на месяц",
            "type": 1,
            "description": """
<b>‼️Предупреждён значит вооружён</b> 😉

Благодаря такому прогнозу сможете:
— скорректировать свои планы, поездки. Так же заранее предпринять действия, для того что бы сохранить свои ресурсы.
— получите подсказки ;
— как обойти острые углы в отношениях (если таковы будут);
— вероятные события;
— какие люди будут учавствовать в вашей жизни и многое другое…

<b>Прогноз</b> является ключом для открытия самой выгодной для Вас двери, и верного выбора пути. 

Чтобы записаться напиши «прогноз на месяц» ⤵️
🙎‍♀️@{worker}
""",
            "amount": "0",
        },
        {
            "name": "Став «Денежный Амулет»",
            "type": 1,
            "description": """
Став «Денежный Амулет» - это нумерологические вибрации и сакральные символы в рамках сакральной геометрии.

Помогает: 
✅ Очистить ваши денежные каналы
✅ Активирует вашу денежную воронку
✅ Став влияет на ваши денежные каналы экологичным способом 

«Денежный Амулет» 
Состоит из ваших персональных цифровых вибраций, которые активируют вашу денежную энергию.

В течение 2-х суток отправляю вам ваши цифровые вибрации насчитанные по вашей дате и инструкцию для Активации.
Став рассчитывается один раз и навсегда. 
Переодически его нужно усиливать.

Чтобы заказать «денежный амулет» пиши мне в личные сообщения  👇🏻

🙎‍♀️@{worker}
         
""",
            "amount": "1500",
        },
        {
            "name": "финансовый код",
            "type": 1,
            "description": """
- Фин.код рассчитан для привлечения финансов на 2024 год. Можно ли расчитывать самостоятельно свой фин.код?
Скажу вам нет, нельзя!

-Фин.код. - состоит из ваших персональных цифровых данных, которые активируют вашу денежную энергию. Так же я заряжаю своей энергией на успех❗️

- После активации данного кода важно видеть и слышать знаки вселенной и быть готовым к новым возможностям, предложениям.

- Также я вам скажу когда нужно активировать свой  фин.код. 

- Для расчета вашего личного финансового кода на 2024 год нужна ваша полная дата рождения (ФИО, день, месяц, год) В течение 2-3х дней я отправляю ваш личный фин.код и инструкцию для активации.

Заказать финансовый код ⤵️
Напишите мне в ЛС «хочу фин.код» 
🙎‍♀️@{worker}
""",
    "amount": "800",
        },
        {
            "name": "Скорая помощь 🚨",
            "type": 1,
            "description": """
Став для привлечения высших сил в важных жизненных ситуациях⬇️

В моменты когда вам хреново, когда у вас важная ситуация, важные жизненные обстоятельства Став дает экстренную помощь. 

Что такое Став? - это графическое изображение.
В него заворачиваться определенным потоком набор энергий через цифровые коды, сакральные символы, геометрические фигуры которые вы должны нарисовать следуя инструкции.
Для каждого Став рассчитывается индивидуально. 
❌ Вы не можете активировать Став за других людей. 
❌ Запрещено 🚫 Активировать Став, чтобы к вам вернулся человек, или с целью наладить отношения с теми, кто от вас ушел.

Чтобы заказать став «скорая помощь» пиши в личные сообщения 👇🏻
🙎‍♀️@{worker}
""",
            "amount": "1800",
        },
        {
            "name": "возврат энергии 🔞",
            "type": 1,
            "description": """
🔞 Возврат своей энергии.

После вступления в близкие отношения мы создаём энергитическую тонкую связь с партнёром, которая не исчезает даже если вы уже расстались. Партнёр питается вашей энергией на протяжении всей своей жизни. За счёт вашей энергии у него открываются многие дороги, потому что вы для него как гинератор! А вы с каждым днём слабеете и закрываете себе дороги удачи, финансы, новые возможности и так же теряете свой ресурс!

Даже если у вас была всего лишь одноразовая встреча, нужно делать отвязку обязательно!

Я как энергопрактик могу это сделать  на тонком плане, и вернуть энергию вам назад! Так же вы делаете маленький ритуал с солью на физическом плане. 

Чтобы заказать возврат своей энергии «отвязка» напишите мне в личные сообщения 👇🏻
🙎‍♀️@{worker}
""",
            "amount": "2100",
        },
        {
            "name": "Полный нумерологический разбор",
            "type": 1,
            "description": """
—Вы узнаете какие энергии на Вас влияют
— какую задачу Вы принесли с собой из прошлого воплощения
— разберем миссию и уровни предназначения
— узнаете в чем Ваша сила и какие есть слабости
— определим слабые стороны здоровья и возможные заболевания.

<b>Бонус</b> 🎁 <b>диагностика чакральной системы. Расскажу над какими нужно работать. </b>

Формат: аудио сообщения в Telegram 

Чтобы заказать полный разбор пиши в личные сообщения «полный разбор» 👇🏻
🙎‍♀️@{worker}
""",
            "amount": "5000",
        },
        {
            "name": "Регрессия/Погружение в подсознание.",
            "type": 1,
            "description": """
<b>Вся работа</b> проводится исключительно с согласия и при вашем активном содействии.

На сессии можно решить ваши волнующие вопросы:
‌На уровне программы личности устранение блоков от негативных установок и страхов в сферах: здоровье, отношение, бизнес, финансы.
‌Чистка от сущностей и блокированных программ. Помощь в расторжении обетов, клятв, зароков в различных религиозных культах, а так же межличностные отношения в прошлых жизнях, блокирующих какую-то сферу в настоящем.
Построение вертикали и восстановление с Высшим Я. Восстановление канала с родной цивилизацией. 
‌Поможем раскрыть и исцелить сердечный канал любви, через который работают все энерго-центры. Если сердечный канал закрыт, то и другие каналы плохо функционирует!
‌Сессия длится 1,5 часа

Чтобы заказать погружение в подсознание пиши в личные сообщения «Сессия»👇🏻

🙎‍♀️@{worker}
""",
            "amount": "8000",
        }
    ]

    for service in services:
        await models.Service.create(**service)

    await message.answer("ok")


@dp.message_handler(IsAdmin(), commands="admin")
async def admin_menu(message: types.Message) -> None:
    markup = await inline.menu_keyboard()
    users = await models.User.query.gino.all()
    await message.answer(
        f"""
Доступное меню: 
Сейчас пользователей: {len(users)}
""",
        reply_markup=markup,
    )


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "admin_menu")
async def admin_menu_c(callback: types.CallbackQuery) -> None:
    markup = await inline.menu_keyboard()

    await callback.message.edit_reply_markup(reply_markup=markup)


# @dp.callback_query_handler(IsAdmin(), lambda c: c.data == "sender")
# async def sender_c(callback: types.CallbackQuery) -> None:
#     markup = await inline.sender_keyboard()

#     await callback.message.edit_reply_markup(reply_markup=markup)


# @dp.callback_query_handler(IsAdmin(), lambda c: c.data == "sender_templates")
# async def sender_ct(callback: types.CallbackQuery, messageId=None) -> None:
#     markup = await inline.sender_templates_keyboard()
#     if messageId is not None:
#         await callback.message.delete()
#         return await callback.message.answer(
#             text="Доступные шаблоны: ", reply_markup=markup
#         )
#     await callback.message.edit_text(text="Доступные шаблоны: ", reply_markup=markup)


# @dp.callback_query_handler(IsAdmin(), lambda c: c.data == "setup_sender")
# async def setup_sender(callback: types.CallbackQuery, state: FSMContext) -> None:
#     CURRENT_STEP = "photo"
#     async with state.proxy() as data:
#         markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP)
#         message = await callback.message.edit_text(
#             "Отправьте фото: ", reply_markup=markup
#         )

#         data["last_message_id"] = message.message_id

#     await SenderState.photo.set()


# @dp.message_handler(
#     IsAdmin(), content_types=[types.ContentType.PHOTO], state=SenderState.photo
# )
# async def setup_sender_photo(message: types.Message, state: FSMContext) -> None:
#     CURRENT_STEP = "text"

#     async with state.proxy() as data:
#         to_change = data.get("to_change")
#         to_change_users = data.get("to_change_users")
#         markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP)
#         if isinstance(message, types.Message):
#             image_path = await image.save(message=message)
#             if to_change is not None:
#                 await models.SenderTemplate.update.values(photo=image_path).where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.status()
#                 template = await models.SenderTemplate.query.where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.first()
#                 await state.finish()

#                 await message.delete()

#                 await ask_for_sender_ready(
#                     message=message,
#                     state=state,
#                     message_id=data["last_message_id"],
#                     new_template=template,
#                     users_template_id=to_change_users,  # TODO
#                 )

#                 return

#             data["photo"] = image_path
#             await message.delete()
#         if data.get("to_change") is not None:
#             markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP, skip=False)
#             message = await message.message.edit_text(
#                 text="Отправьте текст", reply_markup=markup
#             )
#             data["last_message_id"] = message.message_id
#             await SenderState.text.set()
#             return
#         message = await bot.edit_message_text(
#             text="Отправьте текст",
#             chat_id=message.from_user.id,
#             message_id=data.get("last_message_id"),
#             reply_markup=markup,
#         )
#         data["last_message_id"] = message.message_id

#     await SenderState.text.set()


# @dp.message_handler(IsAdmin(), state=SenderState.text)
# async def setup_sender_text(message: types.Message, state: FSMContext) -> None:
#     CURRENT_STEP = "buttons"
#     async with state.proxy() as data:
#         to_change = data.get("to_change")
#         to_change_users = data.get("to_change_users")
#         markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP)
#         if isinstance(message, types.Message):
#             if to_change is not None:
#                 await models.SenderTemplate.update.values(text=message.text).where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.status()
#                 template = await models.SenderTemplate.query.where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.first()
#                 await state.finish()

#                 await message.delete()

#                 await ask_for_sender_ready(
#                     message=message,
#                     state=state,
#                     message_id=data["last_message_id"],
#                     new_template=template,
#                     users_template_id=to_change_users,  # TODO
#                 )

#                 return
#             data["text"] = message.parse_entities()
#             await message.delete()
#         if data.get("to_change") is not None:
#             markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP, skip=False)
#             message = await message.message.edit_text(
#                 text="""
# Отправьте кнопки:

# Формат:
# название/callback
# """,
#                 reply_markup=markup,
#             )
#             data["last_message_id"] = message.message_id
#             await SenderState.buttons.set()
#             return
#         message = await bot.edit_message_text(
#             text="""
# Отправьте кнопки:

# Формат:
# название/callback
# """,
#             chat_id=message.from_user.id,
#             message_id=data.get("last_message_id"),
#             reply_markup=markup,
#         )

#         data["last_message_id"] = message.message_id

#     await SenderState.buttons.set()


# @dp.message_handler(IsAdmin(), state=SenderState.buttons)
# async def setup_sender_buttons(message: types.Message, state: FSMContext) -> None:
#     CURRENT_STEP = "users"
#     async with state.proxy() as data:
#         if isinstance(message, types.Message):
#             to_change = data.get("to_change")
#             if to_change is not None:
#                 await models.SenderTemplate.update.values(buttons=message.text).where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.status()
#                 template = await models.SenderTemplate.query.where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.first()
#                 data["template_id"] = template.idx
#                 await state.finish()

#                 await message.delete()
#                 return
#             data["buttons"] = message.text

#             await message.delete()

#         await state.finish()
#         new_template = await models.SenderTemplate.create(
#             photo=data.get("photo"), text=data.get("text"), buttons=data.get("buttons")
#         )

#         data["template_id"] = new_template.idx

#         await SenderState.users.set()

#         await bot.edit_message_text(
#             text="Выберите пользователей для рассылки: ",
#             chat_id=message.from_user.id,
#             message_id=data.get("last_message_id"),
#             reply_markup=await inline.choose_users_keyboard(new_template.idx),
#         )


# @dp.callback_query_handler(
#     IsAdmin(),
#     lambda c: c.data.startswith("setup_sender_users"),
#     state=SenderState.users,
# )
# async def setup_sender_users(callback: types.CallbackQuery, state: FSMContext) -> None:
#     CURRENT_STEP = 3
#     message = callback
#     splitted_data = callback.data.split("#")
#     users_template_id = splitted_data[2]
#     async with state.proxy() as data:
#         data["users_template_id"] = users_template_id
#         if isinstance(message, types.Message):
#             to_change = data.get("to_change")
#             if to_change is not None:
#                 await models.SenderTemplate.update.values(buttons=message.text).where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.status()
#                 template = await models.SenderTemplate.query.where(
#                     models.SenderTemplate.idx == int(to_change)
#                 ).gino.first()
#                 await state.finish()

#                 await message.delete()

#                 await ask_for_sender_ready(
#                     message=message,
#                     state=state,
#                     message_id=data["last_message_id"],
#                     new_template=template,
#                     users_template_id=users_template_id,
#                 )

#                 return
#             data["buttons"] = message.text

#             await message.delete()

#         await state.finish()
#         new_template = await models.SenderTemplate.create(
#             photo=data.get("photo"), text=data.get("text"), buttons=data.get("buttons")
#         )
#         await ask_for_sender_ready(
#             message=message,
#             state=state,
#             message_id=data.get("last_message_id"),
#             new_template=new_template,
#             users_template_id=users_template_id,
#         )


# async def ask_for_sender_ready(
#     message: types.Message,
#     state: FSMContext,
#     message_id,
#     new_template,
#     users_template_id,
# ):
#     buttons = [
#         f"Да/setup_sender_ready#{new_template.idx}#{users_template_id}",
#         # f"Изменить/setup_sender_change#{new_template.idx}#{users_template_id}",
#         f"Удалить шаблон/setup_sender_delete#{new_template.idx}",
#     ]

#     if isinstance(message, types.CallbackQuery):
#         await message.message.delete()

#     new_message = await sender.custom_send_message(
#         chat_id=message.from_user.id,
#         photo=new_template.photo,
#         text="Вы уверены что хотите начать рассылку?\n\n"
#         + (new_template.text if new_template.text is not None else ""),
#         buttons=(
#             new_template.buttons + "\n" if new_template.buttons is not None else ""
#         )
#         + "\n".join([button for button in buttons]),
#     )
#     await state.set_data({"last_message_id": new_message.message_id})


# @dp.callback_query_handler(
#     IsAdmin(), lambda c: c.data.startswith("setup_sender_delete")
# )
# async def setup_sender_delete(callback: types.CallbackQuery, state: FSMContext):
#     template_id = callback.data.split("#")[-1]
#     await models.SenderTemplate.delete.where(
#         models.SenderTemplate.idx == int(template_id)
#     ).gino.status()

#     await sender_ct(
#         callback=callback, messageId=await state.get_data("last_message_id")
#     )


# @dp.callback_query_handler(
#     IsAdmin(),
#     lambda c: c.data.startswith("setup_sender_skip"),
#     state=SenderState.all_states,
# )
# async def setup_sender_skip(callback: types.CallbackQuery, state: FSMContext):
#     states = {
#         "photo": setup_sender_photo,
#         "text": setup_sender_text,
#         "buttons": setup_sender_buttons,
#     }
#     cstate = callback.data.split("#")[-1]

#     async with state.proxy() as data:
#         data["steps_skipped"] = (
#             data.get("steps_skipped") + f"{cstate},"
#             if data.get("steps_skipped") is not None
#             else f"{cstate},"
#         )

#         if "photo" in data["steps_skipped"] and "text" in data["steps_skipped"]:
#             await state.finish()
#             markup = await inline.sender_keyboard()
#             await bot.edit_message_text(
#                 text="Рассылка не может быть закончена, так как введены только кнопки!\n\nДоступное меню:",
#                 chat_id=callback.from_user.id,
#                 message_id=data["last_message_id"],
#                 reply_markup=markup,
#             )
#             data.clear()
#             return

#     await states[cstate](message=callback, state=state)


# @dp.callback_query_handler(
#     IsAdmin(),
#     lambda c: c.data.startswith("show_template"),
# )
# async def setup_sender_ready(callback: types.CallbackQuery, state: FSMContext):
#     template_id = callback.data.split("#")[-1]
#     template = await models.SenderTemplate.query.where(
#         models.SenderTemplate.idx == int(template_id)
#     ).gino.first()
#     await ask_for_sender_ready(
#         message=callback,
#         state=state,
#         message_id=await state.get_data("last_message_id"),
#         new_template=template,
#         users_template_id="all",  # TODO: sdasd
#     )


# async def get_users_for_template(template_id):
#     users_associated = await models.UserUserTemplateAssociation.query.where(
#         models.UserUserTemplateAssociation.user_template_id == template_id
#     ).gino.all()
#     user_ids = [association.user_id for association in users_associated]

#     associated_users = await models.User.query.where(
#         models.User.idx.in_(user_ids)
#     ).gino.all()
#     return associated_users


# @dp.callback_query_handler(
#     IsAdmin(),
#     lambda c: c.data.startswith("setup_sender_ready"),
# )
# async def setup_sender_ready(callback: types.CallbackQuery):
#     template_id = callback.data.split("#")[1]
#     users_template_id = callback.data.split("#")[2]
#     template = await models.SenderTemplate.query.where(
#         models.SenderTemplate.idx == int(template_id)
#     ).gino.first()
#     users = []
#     if users_template_id == "all":
#         users = await models.User.query.where(models.User.is_active == True).gino.all()
#     else:
#         users = await get_users_for_template(int(users_template_id))
#     if callback.message.caption is None:
#         await callback.message.edit_text("Вы успешно начали рассылку!")
#     else:
#         await callback.message.edit_caption("Вы успешно начали рассылку!")
#     await sender.go(
#         photo=template.photo, text=template.text, buttons=template.buttons, users=users
#     )
#     await callback.message.answer("Рассылка успешно завершена!")


# @dp.callback_query_handler(
#     IsAdmin(),
#     lambda c: c.data.startswith("setup_sender_change"),
# )
# async def setup_sender_change(callback: types.CallbackQuery, state: FSMContext):
#     splitted_data = callback.data.split("#")
#     if not len(splitted_data) > 3:
#         template_id = splitted_data[1]
#         users_template_id = splitted_data[2]
#         markup = await inline.setup_sender_change_keyboard(
#             template_id, users_template_id
#         )
#         await callback.message.delete()
#         new_message = await callback.message.answer(
#             "Что хотите изменить?", reply_markup=markup
#         )
#         await state.set_data({"last_message_id": new_message.message_id})
#         return
#     variant = splitted_data[1]
#     template_id = splitted_data[2]
#     users_template_id = splitted_data[3]

#     await state.set_data(data={"to_change": f"{template_id}"})
#     await state.set_data(data={"to_change_users": f"{users_template_id}"})

#     states = {
#         "photo": setup_sender,
#         "text": setup_sender_photo,
#         "buttons": setup_sender_text,
#     }

#     await states[variant](callback, state=state)


# @dp.callback_query_handler(
#     IsAdmin(), lambda c: c.data == "setup_sender_cancel", state=SenderState.all_states
# )
# async def setup_sender_cancel(callback: types.CallbackQuery, state: FSMContext):
#     markup = await inline.sender_keyboard()

#     await state.finish()
#     await callback.message.edit_text(
#         "Рассылка была отменена! \n\nДоступное меню:", reply_markup=markup
#     )
