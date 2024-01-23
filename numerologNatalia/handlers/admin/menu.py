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
            "name": "Симоронские ритуалы",
            "type": 1,
            "description": """
Если у вас, друзья, возникли какие-то помехи или трудности на жизненном пути, то Симорон-навигатор всегда готов дать вам подсказку. Четко сформулируйте свой запрос и отправьте м не в личные сообщения. Вы получите подсказку, адресованную Вселенной именно вам. От вас  только потребуется проделать то, что предлагается, и вы получите зеленый свет, найдете выход из любых проблемных ситуаций. Очень важно! После исполнения инструкции ( самостоятельно, без зрителей) "похвастаться" перед всеми своим новым амплуа. Вслух или мысленно - в зависимости от обстановки. Так вы утверждаетесь и ваша проблемная личность больше не ставит вам палки в колеса. Даже не сомневайтесь, вас услышат, поддержат, и любые запертые двери откроются перед вами. А все потому, что в каждом человеке дремлет Мастер, ждущий сигнала. 
Отбросьте все ожидания, снимите важность с вашего вопроса. Нужно понимать, что результат может случится не сразу.

Стоимость 1 запроса - 600 руб.
🙎‍♀️@{worker}
""",
            "amount": "0",
        },
        {
            "name": "7 слоёв Кармы",
            "type": 1,
            "description": """
7 слоев Кармы  

  Карма имеет 2 положительных и 5 отрицательных слоев. Каждый человек сам выбирает сценарий Кармы своими поступками, словами, намерением. Чтобы не уйти в отрицательный сценарий, нужно не повторять ошибки прошлого воплощения, не наступать на грабли, которые бросили тогда. Иначе вы запускаете Карму и наказание за повторение ошибокиприлетит с нарастающей силой. Что же делать? Все очень просто - не повторять прошлых ошибок и соблюдать законы Кармы. Ведь основная ее задача не наказать, а предупредить и научить, проработать и развязать кармические узлы. Все они заложены в дате рождения. 
📌 Еще больше информации на моем канале 
https://t.me/numero_logica

Стоимость полного расчета + рекомендация, на что обратить внимание лично тебе - 3420 руб.
🙎‍♀️@{worker}
""",
            "amount": "0",
        },
        {
            "name": "Предназначение и профессия",
            "type": 1,
            "description": """
<b>Предназначение и профессия</b>

Социальная программа человека, пожалуй, – самая важная задача на воплощение в этой жизни. Каждый обязан внести свой вклад в развитие общества. Именно наша социальная задача позволяет не только привести нас к вершине поставленной цели, но и дает силу нашему физическому телу, отвечая за его состояние здоровья.  
Социальная задача – это наше предназначение, задача перед обществом. 
Чтобы узнать свою социальную задачу в этом воплощении и подбор профессий, в которых её можно реализовать, пиши мне дату своего рождения в личные сообщения 👇
🙎‍♀️@{worker}
""",
            "amount": "1500",
        },
        {
            "name": "Предназначение и Призвание",
            "type": 1,
            "description": """
<b>Предназначение и Призвание</b>

В этом воплощении на земле перед нами стоит много задач: родовые, социальные, планетарные… ПРЕДНАЗНАЧЕНИЕ - это одна из таких задач, обязательная  к выполнению. Многие люди на уровне подсознания чувствуют, что занимаются не свои делом и хотят понять в чем же их предназначение. Выполнив своё предназначение можно даже выйти на более высокий уровень и понять, для чего мы пришли в эту жизнь, какое у нас ПРИЗВАНИЕ. 
И всё это можно просчитать по дате рождения и имени.

Пиши мне свои данные в личные сообщения 👇
🙎‍♀️@{worker}
""",
            "amount": "3480",
        },
        {
            "name": "Карта Рождения",
            "type": 1,
            "description": """
Карта Рождения - личный выбор человека. Зная свою задачу на воплощение, он берёт необходимый минимум инструментов ( черт характера и талантов ), без которого не справится в этой миссии. Зачем тащить целый чемодан. Вся эта информация содержится в дате рождения. 
А вот Карта Имени показывает, какими качествами вас хотят наделить родители. 

Пиши мне свои данные в личные сообщения 👇
@{worker}

Стоимость 2-х Карт  - 3480 руб
Стоимость Карты рождения - 1500 руб 
""",
            "amount": "0",
        },
    ]

    for service in services:
        try: 
            await models.Service.create(**service)
        except:
            print(service)

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
            data["text"] = message.parse_entities()
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
