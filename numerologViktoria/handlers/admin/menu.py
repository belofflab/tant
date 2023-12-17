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
            "name": "Консультация по запросу",
            "type": 1,
            "description": """
Разбираем ваш вопрос используя прогностика и другие расчеты. Это может быть любая сфера. 

 На консультацию могу взять не всех, зависит от того, что конкретно вас интересует. 

Стоимость «2000-3500₽»
В зависимости от вопросов.
""",
    "amount": "2000",
        },
        {
            "name": "Предназначение",
            "type": 1,
            "description": """
 Описание Вашего характера. 

- Ваши таланты, способности, скрытый потенциал.

- Разбор по профессиям. 

- Разбор по Карме (проработки которые вы проходите на протяжении жизни и бонусы наработанные в прошлом воплощении)
""",
    "amount": "3120",
        },
        {
            "name": "Совместимость",
            "type": 1,
            "description": """
- Описание вашего характера и характера партнера 

- Ваше поведение  в близких отношениях. (Совместимость по этим показателям) 

- Способ взаимодействия друг с другом, какие проработки.

- Разбор по психотипу (кто вампир кто донор)
- Совместимость по психотипу. 
Все это в аудиоформате ⏏️
""",
    "amount": "2350",
        },
        {
            "name": "1️⃣ Детский разбор",
            "type": 1,
            "description": """
👶Каждый ребёнок приходит в эту жизнь со своим набором качеств, талантов, уроков из прошлой жизни, заложенных в нем при рождении.
‌Задача родителей — научиться понимать своего ребёнка, и помочь ему раскрыться самым благоприятным способом для ребёнка.
‌
✅<b>На консультации вы узнаете:</b>
— таланты и природные склонности вашего ребенка;
— подбор/рекомендации профессий для ребёнка
— какие качества нужно развивать и усиливать, и какие качества, наоборот, мешают;
— как общаться, чтобы понимать своего ребенка;
— какие установки/триггеры могут развиться у Вашего ребёнка- и как этого избежать
— как лучше взаимодействовать именно с вашим ребенком, ваша совместимость;
— какие особенности ребенка следует учитывать;
— кружки, секции, направления, благоприятные сферы для реализации;

<b>Формат:</b> аудио сообщение в WhatsApp 30-50 минут.
🙎‍♀️@{worker}
         
""",
            "amount": "2520",
        },
        {
            "name": "2️⃣ Полный разбор",
            "type": 1,
            "description": """
✅<b>Вы узнаете какие энергии на Вас влияют</b>
— какую задачу Вы принесли с собой из прошлого воплощения
— разберем миссию и уровни предназначения
— узнаете в чем Ваша сила и какие есть слабости
— определим слабые стороны здоровья и возможные заболевания
— получите информацию и поймете на каком уровне вы сейчас находитесь и как поднять свои вибрации, чтобы улучшить все сферы жизни, подружиться с Вашими планетами и раскачать свой денежный потенциал на максимум.
— после консультации и выполнения рекомендаций Ваши энергии станут вашими союзниками судьба будет вам благоволить и вы начнете притягивать удачу. 

Формат: аудио сообщение в Whats App 30-50 минут.
🙎‍♀️@{worker}
""",
            "amount": "4500",
        },
        {
            "name": "3️⃣ Прогноз на 1-2 месяца",
            "type": 1,
            "description": """
✅<b>Благодаря прогнозу Вы можете:</b>
— скорректировать планы, поездки, действия;
— проанализировать финансы и ваши расходы;
— получите подсказку стоит ли совершать ту или иную сделку;
— ознакомится с подводными камнями в отношениях и обойти острые углы;
— заранее предпринять действия, которые сохранят ваши ресурсы, время, деньги, жизненные силы;


В прогнозе будет не только расчёт перспектив, но и совет для вас, и предостережение, которые являются ключами для открытия самой выгодной для Вас двери и самого верного выбора. 

Знакомясь с прогнозом, Вы заранее знаете о тенденциях месяца, и получаете подсказки и пути решения.

Формат: аудио сообщение в Whats App 15-40 минут. 
💰<b>Стоимость прогноза на месяц 750₽/на 2 месяца - 950₽</b>
🙎‍♀️@{worker}
""",
            "amount": "0",
        },
        {
            "name": "4️⃣ Подробный прогноз на год",
            "type": 1,
            "description": """
Прогноз действует с момента когда вы сделали заказ до следующего года этого же месяца. 

Например я делаю прогноз 1.12.23 значит прогноз будет по 1.12.24 года. 
 Полное описание каждого периода  по событиям.
Всего 7 периодов: 
- активный период полон перемен и неожиданностей 
- период женской энергии. Повышение внимание и доверие
- период асгресии и напора
- один из самых удачных периодов в вашем личном году
- кармический период. Возврат Долгов. Повышенная ответственность 
- период необычных знакомств и событий
- мистический период  духовности и иллюзии 

 Рекомендации, предостережения как правильно действовать, чего остерегаться, кто и как на вас повлияет, какие итоги года, как поменяется ваше мышление и какие выводы вы сделаете. 
Главные задачи на 2024 год.

🙎‍♀️@{worker}
""",
            "amount": "7100",
        },
        {
            "name": "5️⃣ Став денежный амулет",
            "type": 1,
            "description": """
<b>Став «Денежный Амулет»</b> - это нумерологические вибрации и сакральные символы в рамках сакральной геометрии.

<b>Помогает: </b>
✅ Очистить ваши денежные каналы
✅ Активирует вашу денежную воронку
✅Вы заметите изменения после первой активации 
✅ Став влияет на ваши денежные каналы экологичным способом 

🧚‍♀️ «Денежный Амулет» - это новый Став🔥 
Он состоит из ваших персональных цифровых вибраций и которые активируют вашу денежную энергию.

В течение 3-х суток отправляю вам ваши цифровые вибрации насчитанные по вашей дате и инструкцию для Активации.
Став рассчитывается один раз и навсегда. 
Переодически его нужно усиливать, я об этом напоминаю на канале. 

🙎‍♀️@{worker}
""",
            "amount": "1500",
        },
        {
            "name": "6️⃣ Финансовый код",
            "type": 1,
            "description": """
<b>Данный 5-значный код рассчитан моей собственной методикой.</b>

-  код рассчитан для привлечения финансов на 2024 год.

Важно слушать и слышать свой внутренний голос и <b>БЫТЬ ОТКРЫТЫМ К НОВЫМ ИДЕЯМ И ПРЕДЛОЖЕНИЯМ.</b>
Возможно ли рассчитать самостоятельно финансовый код изобилия❓
<b>НЕТ!</b>

<b>Финансовый код</b> - это денежная энергия, которая работает по принципу: мы получаем тогда, когда что то отдаём взамен.Произведя оплату финансового кода изобилия он начинает работать на Вас.

Также вы получаете даты в которые можно активировать код. Все даты рассчитываю индивидуально. 

👩‍💻Для расчета вашего личного финансового кода на 2024 год нужна ваша полная дата рождения (день, месяц, год и ФИО)
В течение 3-х дней я отправляю ваш личный рассчитанный код и инструкцию. 
🙎‍♀️@{worker}
""",
            "amount": "800",
        },
        {
            "name": "7️⃣ Став «Помощь»",
            "type": 1,
            "description": """
Чем помогает Став для привлечения высших сил в важных жизненных ситуациях? 

В моменты когда вы не чувствуете поддержки, когда у вас важная ситуация, важные жизненные обстоятельства Став дает экстренную помощь. 

Что такое Став? Это графическое изображение. В него заворачиваться определенным потоком набор энергий через цифровые коды, сакральные символы, геометрические фигуры которые вы должны нарисовать следуя инструкции.
Для каждого Став рассчитывается индивидуально. 
❌ Вы не можете активировать Став за других людей. 
❌ Запрещено 🚫 Активировать Став, чтобы к вам вернулся человек, или с целью наладить отношения с теми, кто от вас ушел. 

У многих из вас уже есть став на привлечение высших сил в сложной жизненной ситуации, этот став модернизирован и теперь вы можете использовать не только в сложной ситуации, но и в любой важной для вас ситуации. 

Для тех у кого став уже есть стоимость новой формулы - 300₽
Для тех кто ранее не приобретал
- 1800₽
🙎‍♀️@{worker}

""",
            "amount": "0",
        },
        {
            "name": "8️⃣ Консультация по запросу",
            "type": 1,
            "description": """
Разбираем ваш вопрос используя прогностика и другие расчеты. Это может быть любая сфера.
На консультацию могу взять не всех, зависит от того, что конкретно вас интересует.
🙎‍♀️@{worker}

""",
            "amount": "3500",
        },
        {
            "name": "9️⃣ Прогноз на 2024 год",
            "type": 1,
            "description": """
То, что вы называете удачей — это по сути правильные действия в правильное время. 
Данный прогноз является инструкцией и вашим персональным объёмом работы на этот год.
Для всего есть своё благоприятное время, покупка машины, запуск бизнеса, инвестиции, недвижимость. 
Если вы выбрали неблагоприятное время, все будет против вас.
🙎‍♀️@{worker}

""",
            "amount": "2024",
        },
        {
            "name": "🔟 Энергетическая отвязка",
            "type": 1,
            "description": """
После вступления в близкие 🔞🤭отношения мы создаём связь с партнёром которая не исчезает даже если вы уже расстались.
Каждый проживает 9-ти летние циклы именно столько и держится энергетическая связь с партнёрами с которыми у вас были отношения 🔞 даже если это была всего лишь одноразовая встреча...
Даже выполняя различные практики которые наполняют энергией или солнцезажигающие действия вы не получаете тот результат который могли, так как часть энергии моментально уходит к бывшим партнерам и чем больше их было тем вы слабее.
Более того вы закрыты для пространства, для новых возможностей, работы, людей и достойных партнёров.
🙎‍♀️@{worker}

""",
            "amount": "1300",
        },
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
Всего пользователей: {len(users)}
Неактивные пользователи {len([user for user in users if not user.is_active])}
""",
        reply_markup=markup,
    )


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "admin_menu")
async def admin_menu_c(callback: types.CallbackQuery) -> None:
    markup = await inline.menu_keyboard()

    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "sender")
async def sender_c(callback: types.CallbackQuery) -> None:
    markup = await inline.sender_keyboard()

    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "sender_templates")
async def sender_ct(callback: types.CallbackQuery, messageId=None) -> None:
    markup = await inline.sender_templates_keyboard()
    if messageId is not None:
        await callback.message.delete()
        return await callback.message.answer(
            text="Доступные шаблоны: ", reply_markup=markup
        )
    await callback.message.edit_text(text="Доступные шаблоны: ", reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == "setup_sender")
async def setup_sender(callback: types.CallbackQuery, state: FSMContext) -> None:
    CURRENT_STEP = "photo"
    async with state.proxy() as data:
        markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP)
        message = await callback.message.edit_text(
            "Отправьте фото: ", reply_markup=markup
        )

        data["last_message_id"] = message.message_id

    await SenderState.photo.set()


@dp.message_handler(
    IsAdmin(), content_types=[types.ContentType.PHOTO], state=SenderState.photo
)
async def setup_sender_photo(message: types.Message, state: FSMContext) -> None:
    CURRENT_STEP = "text"

    async with state.proxy() as data:
        to_change = data.get("to_change")
        to_change_users = data.get("to_change_users")
        markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP)
        if isinstance(message, types.Message):
            image_path = await image.save(message=message)
            if to_change is not None:
                await models.SenderTemplate.update.values(photo=image_path).where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.status()
                template = await models.SenderTemplate.query.where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.first()
                await state.finish()

                await message.delete()

                await ask_for_sender_ready(
                    message=message,
                    state=state,
                    message_id=data["last_message_id"],
                    new_template=template,
                    users_template_id=to_change_users,  # TODO
                )

                return

            data["photo"] = image_path
            await message.delete()
        if data.get("to_change") is not None:
            markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP, skip=False)
            message = await message.message.edit_text(
                text="Отправьте текст", reply_markup=markup
            )
            data["last_message_id"] = message.message_id
            await SenderState.text.set()
            return
        message = await bot.edit_message_text(
            text="Отправьте текст",
            chat_id=message.from_user.id,
            message_id=data.get("last_message_id"),
            reply_markup=markup,
        )
        data["last_message_id"] = message.message_id

    await SenderState.text.set()


@dp.message_handler(IsAdmin(), state=SenderState.text)
async def setup_sender_text(message: types.Message, state: FSMContext) -> None:
    CURRENT_STEP = "buttons"
    async with state.proxy() as data:
        to_change = data.get("to_change")
        to_change_users = data.get("to_change_users")
        markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP)
        if isinstance(message, types.Message):
            if to_change is not None:
                await models.SenderTemplate.update.values(text=message.text).where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.status()
                template = await models.SenderTemplate.query.where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.first()
                await state.finish()

                await message.delete()

                await ask_for_sender_ready(
                    message=message,
                    state=state,
                    message_id=data["last_message_id"],
                    new_template=template,
                    users_template_id=to_change_users,  # TODO
                )

                return
            data["text"] = message.text
            await message.delete()
        if data.get("to_change") is not None:
            markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP, skip=False)
            message = await message.message.edit_text(
                text="""
Отправьте кнопки:

Формат:
название/callback
""",
                reply_markup=markup,
            )
            data["last_message_id"] = message.message_id
            await SenderState.buttons.set()
            return
        message = await bot.edit_message_text(
            text="""
Отправьте кнопки:

Формат:
название/callback
""",
            chat_id=message.from_user.id,
            message_id=data.get("last_message_id"),
            reply_markup=markup,
        )

        data["last_message_id"] = message.message_id

    await SenderState.buttons.set()


@dp.message_handler(IsAdmin(), state=SenderState.buttons)
async def setup_sender_buttons(message: types.Message, state: FSMContext) -> None:
    CURRENT_STEP = "users"
    async with state.proxy() as data:
        if isinstance(message, types.Message):
            to_change = data.get("to_change")
            if to_change is not None:
                await models.SenderTemplate.update.values(buttons=message.text).where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.status()
                template = await models.SenderTemplate.query.where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.first()
                data["template_id"] = template.idx
                await state.finish()

                await message.delete()
                return
            data["buttons"] = message.text

            await message.delete()

        await state.finish()
        new_template = await models.SenderTemplate.create(
            photo=data.get("photo"), text=data.get("text"), buttons=data.get("buttons")
        )

        data["template_id"] = new_template.idx

        await SenderState.users.set()

        await bot.edit_message_text(
            text="Выберите пользователей для рассылки: ",
            chat_id=message.from_user.id,
            message_id=data.get("last_message_id"),
            reply_markup=await inline.choose_users_keyboard(new_template.idx),
        )


@dp.callback_query_handler(
    IsAdmin(),
    lambda c: c.data.startswith("setup_sender_users"),
    state=SenderState.users,
)
async def setup_sender_users(callback: types.CallbackQuery, state: FSMContext) -> None:
    CURRENT_STEP = 3
    message = callback
    splitted_data = callback.data.split("#")
    users_template_id = splitted_data[2]
    async with state.proxy() as data:
        data["users_template_id"] = users_template_id
        if isinstance(message, types.Message):
            to_change = data.get("to_change")
            if to_change is not None:
                await models.SenderTemplate.update.values(buttons=message.text).where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.status()
                template = await models.SenderTemplate.query.where(
                    models.SenderTemplate.idx == int(to_change)
                ).gino.first()
                await state.finish()

                await message.delete()

                await ask_for_sender_ready(
                    message=message,
                    state=state,
                    message_id=data["last_message_id"],
                    new_template=template,
                    users_template_id=users_template_id,
                )

                return
            data["buttons"] = message.text

            await message.delete()

        await state.finish()
        new_template = await models.SenderTemplate.create(
            photo=data.get("photo"), text=data.get("text"), buttons=data.get("buttons")
        )
        await ask_for_sender_ready(
            message=message,
            state=state,
            message_id=data.get("last_message_id"),
            new_template=new_template,
            users_template_id=users_template_id,
        )


async def ask_for_sender_ready(
    message: types.Message,
    state: FSMContext,
    message_id,
    new_template,
    users_template_id,
):
    buttons = [
        f"Да/setup_sender_ready#{new_template.idx}#{users_template_id}",
        # f"Изменить/setup_sender_change#{new_template.idx}#{users_template_id}",
        f"Удалить шаблон/setup_sender_delete#{new_template.idx}",
    ]

    if isinstance(message, types.CallbackQuery):
        await message.message.delete()

    new_message = await sender.custom_send_message(
        chat_id=message.from_user.id,
        photo=new_template.photo,
        text="Вы уверены что хотите начать рассылку?\n\n"
        + (new_template.text if new_template.text is not None else ""),
        buttons=(
            new_template.buttons + "\n" if new_template.buttons is not None else ""
        )
        + "\n".join([button for button in buttons]),
    )
    await state.set_data({"last_message_id": new_message.message_id})


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data.startswith("setup_sender_delete")
)
async def setup_sender_delete(callback: types.CallbackQuery, state: FSMContext):
    template_id = callback.data.split("#")[-1]
    await models.SenderTemplate.delete.where(
        models.SenderTemplate.idx == int(template_id)
    ).gino.status()

    await sender_ct(
        callback=callback, messageId=await state.get_data("last_message_id")
    )


@dp.callback_query_handler(
    IsAdmin(),
    lambda c: c.data.startswith("setup_sender_skip"),
    state=SenderState.all_states,
)
async def setup_sender_skip(callback: types.CallbackQuery, state: FSMContext):
    states = {
        "photo": setup_sender_photo,
        "text": setup_sender_text,
        "buttons": setup_sender_buttons,
    }
    cstate = callback.data.split("#")[-1]

    async with state.proxy() as data:
        data["steps_skipped"] = (
            data.get("steps_skipped") + f"{cstate},"
            if data.get("steps_skipped") is not None
            else f"{cstate},"
        )

        if "photo" in data["steps_skipped"] and "text" in data["steps_skipped"]:
            await state.finish()
            markup = await inline.sender_keyboard()
            await bot.edit_message_text(
                text="Рассылка не может быть закончена, так как введены только кнопки!\n\nДоступное меню:",
                chat_id=callback.from_user.id,
                message_id=data["last_message_id"],
                reply_markup=markup,
            )
            data.clear()
            return

    await states[cstate](message=callback, state=state)


@dp.callback_query_handler(
    IsAdmin(),
    lambda c: c.data.startswith("show_template"),
)
async def setup_sender_ready(callback: types.CallbackQuery, state: FSMContext):
    template_id = callback.data.split("#")[-1]
    template = await models.SenderTemplate.query.where(
        models.SenderTemplate.idx == int(template_id)
    ).gino.first()
    await ask_for_sender_ready(
        message=callback,
        state=state,
        message_id=await state.get_data("last_message_id"),
        new_template=template,
        users_template_id="all",  # TODO: sdasd
    )


async def get_users_for_template(template_id):
    users_associated = await models.UserUserTemplateAssociation.query.where(
        models.UserUserTemplateAssociation.user_template_id == template_id
    ).gino.all()
    user_ids = [association.user_id for association in users_associated]

    associated_users = await models.User.query.where(
        models.User.idx.in_(user_ids)
    ).gino.all()
    return associated_users


@dp.callback_query_handler(
    IsAdmin(),
    lambda c: c.data.startswith("setup_sender_ready"),
)
async def setup_sender_ready(callback: types.CallbackQuery):
    template_id = callback.data.split("#")[1]
    users_template_id = callback.data.split("#")[2]
    template = await models.SenderTemplate.query.where(
        models.SenderTemplate.idx == int(template_id)
    ).gino.first()
    users = []
    if users_template_id == "all":
        users = await models.User.query.where(models.User.is_active == True).gino.all()
    else:
        users = await get_users_for_template(int(users_template_id))
    if callback.message.caption is None:
        await callback.message.edit_text("Вы успешно начали рассылку!")
    else:
        await callback.message.edit_caption("Вы успешно начали рассылку!")
    await sender.go(
        photo=template.photo, text=template.text, buttons=template.buttons, users=users
    )
    await callback.message.answer("Рассылка успешно завершена!")


@dp.callback_query_handler(
    IsAdmin(),
    lambda c: c.data.startswith("setup_sender_change"),
)
async def setup_sender_change(callback: types.CallbackQuery, state: FSMContext):
    splitted_data = callback.data.split("#")
    if not len(splitted_data) > 3:
        template_id = splitted_data[1]
        users_template_id = splitted_data[2]
        markup = await inline.setup_sender_change_keyboard(
            template_id, users_template_id
        )
        await callback.message.delete()
        new_message = await callback.message.answer(
            "Что хотите изменить?", reply_markup=markup
        )
        await state.set_data({"last_message_id": new_message.message_id})
        return
    variant = splitted_data[1]
    template_id = splitted_data[2]
    users_template_id = splitted_data[3]

    await state.set_data(data={"to_change": f"{template_id}"})
    await state.set_data(data={"to_change_users": f"{users_template_id}"})

    states = {
        "photo": setup_sender,
        "text": setup_sender_photo,
        "buttons": setup_sender_text,
    }

    await states[variant](callback, state=state)


@dp.callback_query_handler(
    IsAdmin(), lambda c: c.data == "setup_sender_cancel", state=SenderState.all_states
)
async def setup_sender_cancel(callback: types.CallbackQuery, state: FSMContext):
    markup = await inline.sender_keyboard()

    await state.finish()
    await callback.message.edit_text(
        "Рассылка была отменена! \n\nДоступное меню:", reply_markup=markup
    )
