from aiogram import types

from database import models
from keyboards.admin import inline
from loader import dp, bot
from states.sender import Sender as SenderState
from utils import image, sender

from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == "sender")
async def sender_c(callback: types.CallbackQuery) -> None:
    markup = await inline.sender_keyboard()

    await callback.message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "sender_templates")
async def sender_ct(callback: types.CallbackQuery, messageId=None) -> None:
    markup = await inline.sender_templates_keyboard()
    if messageId is not None:
        await callback.message.delete()
        return await callback.message.answer(
            text="Доступные шаблоны: ", reply_markup=markup
        )
    await callback.message.edit_text(text="Доступные шаблоны: ", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == "setup_sender")
async def setup_sender(callback: types.CallbackQuery, state: FSMContext) -> None:
    CURRENT_STEP = "photo"
    async with state.proxy() as data:
        markup = await inline.cancel_or_skip_keyboard(step=CURRENT_STEP)
        message = await callback.message.edit_text(
            "Отправьте фото: ", reply_markup=markup
        )

        data["last_message_id"] = message.message_id

    await SenderState.photo.set()


@dp.message_handler(content_types=[types.ContentType.PHOTO], state=SenderState.photo)
async def setup_sender_photo(message: types.Message, state: FSMContext) -> None:
    CURRENT_STEP = "text"

    async with state.proxy() as data:
        to_change = data.get("to_change")
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


@dp.message_handler(state=SenderState.text)
async def setup_sender_text(message: types.Message, state: FSMContext) -> None:
    CURRENT_STEP = "buttons"
    async with state.proxy() as data:
        to_change = data.get("to_change")
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


@dp.message_handler(state=SenderState.buttons)
async def setup_sender_buttons(message: types.Message, state: FSMContext) -> None:
    CURRENT_STEP = 3
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
                await state.finish()
                await message.delete()
                await ask_for_sender_ready(
                    message=message,
                    state=state,
                    message_id=data["last_message_id"],
                    new_template=template,
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
        )


async def ask_for_sender_ready(
    message: types.Message, state: FSMContext, message_id, new_template
):
    buttons = [
        f"Да/setup_sender_ready#{new_template.idx}",
        f"Изменить/setup_sender_change#{new_template.idx}",
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


@dp.callback_query_handler(lambda c: c.data.startswith("setup_sender_delete"))
async def setup_sender_delete(callback: types.CallbackQuery, state: FSMContext):
    template_id = callback.data.split("#")[-1]
    await models.SenderTemplate.delete.where(
        models.SenderTemplate.idx == int(template_id)
    ).gino.status()

    await sender_ct(
        callback=callback, messageId=await state.get_data("last_message_id")
    )


@dp.callback_query_handler(
    lambda c: c.data.startswith("setup_sender_skip"), state=SenderState.all_states
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
    )


@dp.callback_query_handler(
    lambda c: c.data.startswith("setup_sender_ready"),
)
async def setup_sender_ready(callback: types.CallbackQuery):
    template_id = callback.data.split("#")[-1]
    template = await models.SenderTemplate.query.where(
        models.SenderTemplate.idx == int(template_id)
    ).gino.first()
    await sender.go(photo=template.photo, text=template.text, buttons=template.buttons)
    await callback.message.edit_text("Вы успешно начали рассылку!")


@dp.callback_query_handler(
    lambda c: c.data.startswith("setup_sender_change"),
)
async def setup_sender_change(callback: types.CallbackQuery, state: FSMContext):
    splitted_data = callback.data.split("#")
    if not len(splitted_data) > 2:
        template_id = splitted_data[-1]
        markup = await inline.setup_sender_change_keyboard(template_id)
        await callback.message.delete()
        new_message = await callback.message.answer(
            "Что хотите изменить?", reply_markup=markup
        )
        await state.set_data({"last_message_id": new_message.message_id})
        return
    variant = splitted_data[1]
    template_id = splitted_data[2]

    await state.set_data(data={"to_change": f"{template_id}"})

    states = {
        "photo": setup_sender,
        "text": setup_sender_photo,
        "buttons": setup_sender_text,
    }

    await states[variant](callback, state=state)


@dp.callback_query_handler(
    lambda c: c.data == "setup_sender_cancel", state=SenderState.all_states
)
async def setup_sender_cancel(callback: types.CallbackQuery, state: FSMContext):
    markup = await inline.sender_keyboard()

    await state.finish()
    await callback.message.edit_text(
        "Рассылка была отменена! \n\nДоступное меню:", reply_markup=markup
    )
