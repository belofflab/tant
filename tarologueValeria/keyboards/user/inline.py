from database import models
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

service_cd = CallbackData("show_service", "level", "worker", "type", "service")
askeza_cd = CallbackData(
    "show_askeza", "level", "worker", "content_type", "content_page"
)
hyromantia_cd = CallbackData(
    "show_hyromantia", "level", "worker", "content_type", "content_page"
)

def make_service_cd(level, worker="taro2_sashA", type="0", service="0"):
    return service_cd.new(level=level, worker=worker, type=type, service=service)

def make_askeza_cd(level, worker="0", content_type="0", content_page="1"):
    return askeza_cd.new(
        level=level, worker=worker, content_type=content_type, content_page=content_page
    )

def make_hyromantia_cd(level, worker="0", content_type="0", content_page="1"):
    return hyromantia_cd.new(
        level=level, worker=worker, content_type=content_type, content_page=content_page
    )


async def free_markup(worker: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="Назад", callback_data=make_service_cd(CURRENT_LEVEL - 1, worker=worker)
        )
    )

    return markup


async def menu_keyboard(worker: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()
    buttons = [
        {
            "text": "Аскеза на желание 👑",
            "callback_data": make_askeza_cd(level=CURRENT_LEVEL + 1, worker=worker),
        },
        {
            "text": "Хиромантия 🖐️",
            "callback_data": make_hyromantia_cd(level=CURRENT_LEVEL + 1, worker=worker),
        },
        {"text": "Бесплатная консультация 👩‍💻", "callback_data": f"free#{worker}"},
        {
            "text": "Все услуги 📄",
            "callback_data": make_service_cd(level=CURRENT_LEVEL + 1, worker=worker),
        },
        {"text": "Телеграм канал", "url": "https://t.me/tvoi_tarollogg"},
        {"text": "ХОЧУ В КОМАНДУ", "callback_data": f"wanttoteam#{worker}"},
    ]
    for button in buttons:
        markup.row(InlineKeyboardButton(**button))
    return markup


async def service_types_keyboard(worker: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()
    service_types = await models.ServiceType.query.gino.all()
    for service_type in service_types:
        markup.row(
            InlineKeyboardButton(
                text=service_type.name,
                callback_data=make_service_cd(
                    CURRENT_LEVEL + 1, worker, service_type.idx
                ),
            )
        )
    markup.add(
        InlineKeyboardButton(
            text="Назад", callback_data=make_service_cd(CURRENT_LEVEL - 1, worker=worker)
        )
    )
    return markup


async def services_keyboard(service_type: str, worker: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    service_type = 1
    markup = InlineKeyboardMarkup()
    services = await models.Service.query.where(
        models.Service.type == int(service_type)
    ).gino.all()
    for idx, service in enumerate(services):
        if idx == 2 and int(service_type) == 1:
            markup.insert(
                InlineKeyboardButton(
                    text=service.name,
                    callback_data=make_service_cd(
                        CURRENT_LEVEL + 1,
                        worker=worker,
                        type=service_type,
                        service=service.idx,
                    ),
                )
            )
        else:
            markup.row(
                InlineKeyboardButton(
                    text=service.name,
                    callback_data=make_service_cd(
                        CURRENT_LEVEL + 1,
                        worker=worker,
                        type=service_type,
                        service=service.idx,
                    ),
                )
            )
    markup.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_service_cd(
                CURRENT_LEVEL - 1, worker=worker, type=service_type
            ),
        )
    )
    return markup


async def show_service(
    service_type: str, service: str, worker: str
) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_service_cd(
                CURRENT_LEVEL - 1, worker=worker, type=service_type, service=service
            ),
        )
    )
    return markup
