import requests
from database import models
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from data.config import SERVER_URL
from math import ceil

service_cd = CallbackData("show_service", "level", "worker", "type", "service")
bonus_cd = CallbackData("show_bonus", "level", "worker", "month")
matrix_cd = CallbackData(
    "show_matrix", "level", "worker", "page", "request_id", "matrix_page"
)
relationships_cd = CallbackData("show_relationships", "level", "worker", "key")
askeza_cd = CallbackData(
    "show_askeza", "level", "worker", "content_type", "content_page"
)
training_cd = CallbackData(
    "show_training", "level", "worker"
)


def make_service_cd(level, worker="viktoria_numer", type="0", service="0"):
    return service_cd.new(level=level, worker=worker, type=type, service=service)


def make_bonus_cd(level, worker="viktoria_numer", month="0"):
    return bonus_cd.new(level=level, worker=worker, month=month)


def make_relationships_cd(level, worker="viktoria_numer", key="0"):
    return relationships_cd.new(level=level, worker=worker, key=key)


def make_askeza_cd(level, worker="0", content_type="0", content_page="1"):
    return askeza_cd.new(
        level=level, worker=worker, content_type=content_type, content_page=content_page
    )


def make_matrix_cd(level, page="1", worker="0", request_id="0", matrix_page="1"):
    return matrix_cd.new(
        level=level,
        request_id=request_id,
        worker=worker,
        page=page,
        matrix_page=matrix_page,
    )

def make_training_cd(level, worker="0"):
    return training_cd.new(level=level, worker=worker)

async def free_markup(worker: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_service_cd(CURRENT_LEVEL - 1, worker=worker),
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
        {"text": "Бесплатная консультация 🗣", "callback_data": f"free#{worker}"},
        {
            "text": "Мои услуги 💫",
            "callback_data": make_service_cd(level=CURRENT_LEVEL + 1, worker=worker),
        },
        # {
        #     "text": "Матрица пифагора 🧠",
        #     "callback_data": make_matrix_cd(level=CURRENT_LEVEL + 1, worker=worker),
        # },
        {
            "text": "обучение Таро 🧑‍🎓",
            "callback_data": make_training_cd(level=CURRENT_LEVEL + 1, worker=worker)
        },
        {"text": "Мой канал 📣", "url": "https://t.me/+QZHX8A719dUyZmRi"},
        # {"text": "Чат общения 👥", "url": "https://t.me/obschenie_kanal"},
        {"text": "Связаться со мной 📩", "url": "https://t.me/valentina_numerologEnerg"},
        # {"text": "Мой сайт", "url": "https://taplink.cc/numerolog_viktoria.nikonova_"},
        {"text": "Бонусы 🎁", "callback_data": f"bonus#{worker}"},
    ]
    for button in buttons:
        markup.row(InlineKeyboardButton(**button))
    return markup


async def list_matrix(worker: int, user_id: int, current_page: str = "1"):
    response = requests.get(SERVER_URL + f"/matrix/requests/user/{user_id}/")
    matrixes = response.json()
    CURRENT_LEVEL = 1
    MAX_ITEMS_PER_PAGE = 2
    MAX_PAGES = ceil(len(matrixes) / MAX_ITEMS_PER_PAGE)
    markup = InlineKeyboardMarkup(row_width=3)
    current_page = int(current_page)
    next_page = matrixes[
        (current_page * MAX_ITEMS_PER_PAGE)
        - MAX_ITEMS_PER_PAGE : current_page * MAX_ITEMS_PER_PAGE
    ]
    markup.add(
        InlineKeyboardButton(
            **{
                "text": "Заказать матрицу 🍀",
                "callback_data": f"order_matrix#{worker}",
            }
        )
    )
    for matrix in next_page:
        markup.row(
            InlineKeyboardButton(
                text=f"{matrix.get('dob')}",
                callback_data=make_matrix_cd(
                    CURRENT_LEVEL + 1,
                    worker=worker,
                    request_id=matrix.get("id"),
                    page=current_page,
                ),
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=make_matrix_cd(
                level=CURRENT_LEVEL,
                page=(current_page - 1) if current_page != 1 else current_page,
                worker=worker,
            ),
        )
    )
    markup.insert(
        InlineKeyboardButton(text=f"{current_page}/{MAX_PAGES}", callback_data="...")
    )

    markup.insert(
        InlineKeyboardButton(
            text=">>",
            callback_data=make_matrix_cd(
                level=CURRENT_LEVEL,
                page=(current_page + 1)
                if not current_page >= MAX_PAGES
                else current_page,
                worker=worker,
            ),
        )
    )

    markup.add(
        InlineKeyboardButton(
            text="Назад", callback_data=make_matrix_cd(CURRENT_LEVEL - 1, worker=worker)
        )
    )

    return markup


async def show_matrix(
    worker: int, page: int, request_id: int, matrix_page: int, max_pages: int
):
    markup = InlineKeyboardMarkup(row_width=3)
    CURRENT_LEVEL = 2
    MAX_PAGES = int(max_pages)
    current_page = int(matrix_page)
    markup.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=make_matrix_cd(
                level=CURRENT_LEVEL,
                page=page,
                request_id=request_id,
                matrix_page=(current_page - 1) if current_page != 1 else current_page,
                worker=worker,
            ),
        )
    )
    markup.insert(
        InlineKeyboardButton(text=f"{current_page}/{MAX_PAGES}", callback_data="...")
    )

    markup.insert(
        InlineKeyboardButton(
            text=">>",
            callback_data=make_matrix_cd(
                level=CURRENT_LEVEL,
                page=page,
                request_id=request_id,
                matrix_page=(current_page + 1)
                if not current_page >= MAX_PAGES
                else current_page,
                worker=worker,
            ),
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_matrix_cd(CURRENT_LEVEL - 1, worker=worker, page=page),
        )
    )

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
            text="Назад",
            callback_data=make_service_cd(CURRENT_LEVEL - 1, worker=worker),
        )
    )
    return markup


async def services_keyboard(service_type: str, worker: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    services = await models.Service.query.where(
        models.Service.type == int(service_type)
    ).gino.all()
    for idx, service in enumerate(services):
        if idx == 2:
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
    q_service = await models.Service.query.where(
        models.Service.idx == int(service)
    ).gino.first()
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        # InlineKeyboardButton(
        #     text="Записаться на разбор",
        #     url="https://api.whatsapp.com/send/?phone=79292084866&text=Привет!+Хочу+{text}&type=phone_number&app_absent=0?".format(
        #         text=q_service.name.replace("«", "").replace("»", "").replace(" ", "+")
        #     ),
        # ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_service_cd(
                CURRENT_LEVEL - 1, worker=worker, type=service_type, service=service
            ),
        ),
    )
    return markup


async def confirm_deposit_request_keyboard(
    mrequest_id: int, wrequest_id: int, edit_message: int, user_id: int, worker: str
):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {
            "text": "Подвердить ✅",
            "callback_data": f"deposit_request_confirm#{mrequest_id}#{wrequest_id}#{edit_message}#{user_id}#{worker}",
        },
        {
            "text": "Отклонить ❌",
            "callback_data": f"deposit_request_decline#{mrequest_id}#{wrequest_id}#{edit_message}#{user_id}#{worker}",
        },
    ]
    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))

    return markup

async def training_request_keyboard(
    wrequest_id: int, edit_message: int, user_id: int, worker: str
):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {
            "text": "Подвердить ✅",
            "callback_data": f"training_request_confirm#{wrequest_id}#{edit_message}#{user_id}#{worker}",
        },
        {
            "text": "Отклонить ❌",
            "callback_data": f"training_request_decline#{wrequest_id}#{edit_message}#{user_id}#{worker}",
        },
    ]
    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))

    return markup
