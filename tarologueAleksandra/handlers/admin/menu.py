from aiogram import types

from database import models
from keyboards.admin import inline
from loader import dp, bot
from states.sender import Sender as SenderState
from utils import image, sender, formatter
from filters.is_admin import IsAdmin
from aiogram.dispatcher import FSMContext


@dp.message_handler(IsAdmin(), commands="setup")
async def setup(message: types.Message) -> None:
    service_types = [{"idx": 1, "name": "Консультации"}, {"idx": 2, "name": "Ритуалы"}]

    for service_type in service_types:
        await models.ServiceType.create(**service_type)

    services = [
        {
            "name": "Всё обо мне",
            "type": 1,
            "description": """
<b>В этом разборе мы детально разберем данные темы👇🏻</b>
         
1. Какие аспекты моей личности я должен лучше понять?
2. Какие таланты и способности я не использую в полной мере?
3. Какие прошлые опыты оказывают влияние на мое текущее состояние?
4. Какие страхи или сомнения могут сдерживать мой личностный рост?
5. Какие аспекты моей жизни требуют большего внимания и развития?
6. Какие жизненные ценности для меня наиболее важны?
7. Как я могу лучше управлять своими эмоциями и стрессом?
8. Какие отношения и взаимодействия в моей жизни могут быть улучшены?
9. Какие новые возможности или направления развития могут открыться для меня?
10. Какие шаги или действия я могу предпринять, чтобы достичь более гармоничной и удовлетворительной жизни?
         
Напишите «Разбор Все обо мне» 👇🏻
🙎‍♀️@{worker}
         
""",
            "amount": "2000",
        },
        {
            "name": "Один вопрос 🙋🏻‍♀️",
            "type": 1,
            "description": """
- Напишите «Хочу ответ на один вопрос» сформулируйте свой вопрос, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻
 
🙎‍♀️@{worker}
""",
            "amount": "500",
        },
        {
            "name": "Два вопроса 🙋🏻‍♀️",
            "type": 1,
            "description": """
- Напишите «Хочу ответ на два вопроса» сформулируйте свой вопрос, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻

🙎‍♀️@{worker}
""",
            "amount": "750",
        },
        {
            "name": "Три вопроса 🙋🏻‍♀️",
            "type": 1,
            "description": """
- Напишите «Хочу ответ на три вопроса» сформулируйте свои вопросы, напишите дату рождения и пришлите свое фото. Все это направьте 👇🏻

🙎‍♀️@{worker}
""",
            "amount": "1050",
        },
        {
            "name": "🌸Прогноз на год",
            "type": 1,
            "description": """
1. Какие важные жизненные уроки я должен усвоить в этом году?
2. Каковы мои ключевые цели и задачи на этот год?
3. Какие возможности ждут меня в ближайшем будущем?
4. Каковы преграды или вызовы, которые я, возможно, встречу в этом году?
5. Каковы темы, которые будут центральными для моего эмоционального и духовного развития в этом году?
6. Какой аспект моей жизни потребует особого внимания в ближайшем будущем?
7. Какие изменения и трансформации ждут меня в этом году?
8. Каким образом я могу развить свои таланты и навыки в течение года?
9. Какие ключевые решения и поворотные точки ожидают меня в этом году?
10. Каковы возможные исходы моих текущих проектов и начинаний на этот год?
11. К дополнению рассмотрим любые ваши вопросы
💥 Для заказа прогноза пишите мне в личные сообщения 👇👇👇
🙎‍♀️@{worker}
""",
    "amount": "5500",
        },
        {
            "name": "Детский разбор от 0 до 3",
            "type": 1,
            "description": """
<b>Детский разбор от 0 до 3</b>

Что входит в разбор 👇🏻

1. Каково общее состояние моего малыша на данный момент?
2. Какие аспекты развития моего малыша требуют особого внимания?
3. Как я могу поддержать здоровье и благополучие моего малыша?
4. Какие игры или занятия могут помочь развить навыки и интересы моего малыша?
5. Как я могу создать безопасное и любящее окружение для моего малыша?
6. Какие аспекты воспитания могут быть особенно важными для моего ребенка на данный момент?
7. Какие уроки жизни могут быть полезными для моего малыша на этой стадии его развития?
8. Как я могу поддерживать эмоциональное благополучие моего малыша и помогать ему выражать свои чувства?

Напишите мне @{worker} «Детский разбор от 0 до 3»
""",
            "amount": "2000",
        },
        {
            "name": "Детский разбор от 3 лет",
            "type": 1,
            "description": """
<b>«Детский разбор от 3»</b>

1. Как я могу лучше понять своего ребенка?
2. Какие аспекты воспитания нуждаются в моем внимании?
3. Каковы сильные стороны моего ребенка, которые стоит развивать?
4. Как я могу помочь своему ребенку развить самоуверенность?
5. Каковы лучшие способы обучения и образования для моего ребенка?
6. Какие преграды могут возникнуть в будущем, и как их можно преодолеть?
7. Как я могу создать более гармоничные отношения с моим ребенком?
8. Какие уроки жизни важно усвоить моему ребенку на данный момент?

Напишите мне @{worker} «Детский разбор от 3»
""",
            "amount": "2000",
        },
        {
            "name": "Глубокий анализ отношений 🔍",
            "type": 1,
            "description": """
<b>В этом разборе мы детально разберем данные темы👇🏻</b>

1. Какие энергии влияют на мои отношения в данный момент?
2. Какие аспекты моей личности могут влиять на развитие отношений?
3. Какие вызовы или преграды стоят на пути к гармоничным отношениям?
4. Какова динамика отношений между мной и моим партнером/партнеркой?
5. Какие аспекты нашей связи нуждаются в укреплении или изменении?
6. Какие уроки или опыт я могу извлечь из моих текущих отношений?
7. Какие действия мне следует предпринять, чтобы улучшить мои отношения?
8. Какие пути к разрешению конфликтов или недопониманий можно применить?
9. Какие изменения могут произойти в моих отношениях в ближайшем будущем?
10. Какие возможности или перспективы открываются передо мной в контексте моих отношений?
11. Перспективы развития отношений 6 месяцев.

Напишите 👇🏻
@{worker} «Разбор Глубокий анализ отношений»

""",
            "amount": "2000",
        },
        {
            "name": "Сложная жизненная ситуация 🙈",
            "type": 1,
            "description": """
<b>«Сложная жизненная ситуация»</b>

1. Какова природа этой сложной ситуации?
2. Какие факторы или обстоятельства привели к возникновению этой проблемы?
3. Какие аспекты ситуации я должен учесть, чтобы справиться с ней наилучшим образом?
4. Какие уроки или опыт я могу извлечь из этой ситуации?
5. Какие ресурсы или поддержку мне следует использовать для решения проблемы?
6. Какие действия я могу предпринять, чтобы изменить ход событий в свою пользу?
7. Какие возможные исходы могут ожидать меня в будущем, если я останусь в этой ситуации?
8. Какие аспекты собственной личности или поведения могут влиять на разрешение этой проблемы?
9. Какие шаги или решения могут привести к более гармоничному развитию событий?
10. Как я могу использовать этот опыт для своего долгосрочного роста и самосовершенствования?

Напишите 👇🏻
@{worker} «Разбор Сложная жизненная ситуация»

""",
            "amount": "2000",
        },
        {
            "name": "Созвон 📱",
            "type": 1,
            "description": """
<b>•30 минут—2000₽</b>
<b>•60 минут— 3000₽</b>
<b>•90 минут—4500₽</b>

Напишите слово «Созвон» и количество минут.👇🏻

🙎‍♀️@{worker}

""",
            "amount": "0",
        },
        {
            "name": "Эмоциональная отвязка",
            "type": 2,
            "description": """
<b>Эмоциональная отвязка</b>

Эмоциональная отвязка с помощью свечи является частью магической практики, направленной на разрыв эмоциональной связи с определенным человеком или событием.

Этот процесс может быть выполнен один раз или несколько раз, в зависимости от вашей потребности. Важно помнить, что эмоциональная отвязка может потребовать времени и практики.

Напиши мне в директ слово «Отвязка»
👇👇👇
 
🕯️@{worker}
""",
            "amount": "2000",
        },
        {
            "name": "Открытие финансового потока",
            "type": 2,
            "description": """
<b>Открытие финансового потока</b>

Мощная свечная магия, направленная на привлечение богатства и открытия финансового потока. 

Напишите мне в личные сообщения слово 
«Финансовый поток»
👇👇👇

🕯️@{worker}
""",
            "amount": "2000",
        },
        {
            "name": "Снятие негатива",
            "type": 2,
            "description": """
<b>Снятие негатива</b>

Данный мощный метод практики сжигает весь негатив в вашем поле, освобождает новые пути, снимает стресс, тревогу и депрессию. Освобождает от негативных привязанностей. 

Напиши мне в личные сообщения слово 
«Чистка»
👇👇👇

🕯️@{worker}
""",
            "amount": "2000",
        },
        {
            "name": "❤️Привлечение любви",
            "type": 2,
            "description": """
<b>❤️Привлечение любви</b>

Мощный метод ритуала по привлечению любви в вашу жизнь и раскрытию сексуального потока 

Напишите мне в личные сообщения слово
 «Любовь»
👇👇👇
 
🕯️@{worker}
""",
            "amount": "2000",
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
Сейчас пользователей: {len(users)}
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
            data["text"] = formatter.texttohtml(message)
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
    await callback.message.answer("Рассылка завершена успешно!")


@dp.callback_query_handler(
    IsAdmin(),
    lambda c: c.data.startswith("setup_sender_change"),
)
async def setup_sender_change(callback: types.CallbackQuery, state: FSMContext):
    splitted_data = callback.data.split("#")
    if not len(splitted_data) > 3:
        template_id = splitted_data[1]
        users_template_id = splitted_data[2]
        markup = await inline.setup_sender_change_keyboard(template_id, users_template_id)
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
