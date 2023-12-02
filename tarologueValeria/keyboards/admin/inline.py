from database import models
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.callback_data import CallbackData


async def menu_keyboard():
    markup = InlineKeyboardMarkup()

    buttons = [
        {"text": "Рассылка", "callback_data": "sender"},
        {
            "text": "Аналитика",
            "web_app": WebAppInfo(
                url="https://tant.belofflab.com/api/v1/analytics/info/"
            ),
        },
    ]

    for button in buttons:
        markup.add(InlineKeyboardButton(**button))

    return markup


async def sender_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Создать рассылку", "callback_data": "setup_sender"},
        {"text": "Шаблоны", "callback_data": "sender_templates"},
    ]

    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))
    markup.row(InlineKeyboardButton(text="Назад", callback_data="admin_menu"))

    return markup


async def sender_templates_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    templates = await models.SenderTemplate.query.gino.all()

    for template in templates:
        markup.insert(
            InlineKeyboardButton(
                text=template.text[:20]
                if template.text is not None
                else str(template.date),
                callback_data=f"show_template#{template.idx}",
            )
        )

    markup.row(InlineKeyboardButton(text="Назад", callback_data="sender"))

    return markup

async def choose_users_keyboard(template_id: str):
    markup = InlineKeyboardMarkup(row_width=2)
    user_templates = await models.UserTemplate.query.order_by(models.UserTemplate.date.desc()).gino.all()
    markup.add(InlineKeyboardButton(
        text="Все",
        callback_data=f"setup_sender_users#{template_id}#all"
    ))

    for user_template in user_templates:
        markup.add(
            InlineKeyboardButton(
                text=user_template.name[:20],
                callback_data=f"setup_sender_users#{template_id}#{user_template.idx}"
            )
        )

    return markup



async def cancel_or_skip_keyboard(step: str, skip=True):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Отменить", "callback_data": "setup_sender_cancel"},
    ]

    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))

    if skip:
        markup.insert(
            InlineKeyboardButton(
                **{"text": "Пропустить", "callback_data": f"setup_sender_skip#{step}"}
            )
        )

    return markup


async def setup_sender_change_keyboard(template_id: str, users_template_id: str):
    buttons = [
        {"text": "Фото", "callback_data": f"setup_sender_change#photo#{template_id}#{users_template_id}"},
        {"text": "Текст", "callback_data": f"setup_sender_change#text#{template_id}#{users_template_id}"},
        {
            "text": "Кнопки",
            "callback_data": f"setup_sender_change#buttons#{template_id}#{users_template_id}",
        },
    ]

    markup = InlineKeyboardMarkup(row_width=3)

    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))

    markup.row(
        InlineKeyboardButton(
            **{"text": "Смотреть все шаблоны", "callback_data": "sender_templates"}
        )
    )

    return markup

