import requests
from math import ceil
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import SERVER_URL
from aiogram.utils.callback_data import CallbackData

workers_cd = CallbackData("show_workers", "level", "page", "worker")
workers_requests_cd = CallbackData("show_workers_requests", "level", "page", "request")
payment_details_cd = CallbackData("show_payment_details", "level", "detail")
cashier_cd = CallbackData("show_cashier", "level", "type", "amount")
proxy6_cd = CallbackData("show_proxy6", "level", "proxy")


def make_workers_cd(level, page="1", worker="0"):
    return workers_cd.new(level=level, page=page, worker=worker)


def make_workers_requests_cd(level, page="1", request="0"):
    return workers_requests_cd.new(level=level, page=page, request=request)


def make_payment_details_cd(level, detail="0"):
    return payment_details_cd.new(level=level, detail=detail)

def make_cashier_cd(level, type="-", amount="0"):
    return cashier_cd.new(level=level, type=type, amount=amount)

def make_proxy6_cd(level, proxy="0"):
    return proxy6_cd.new(level=level, proxy=proxy)


async def admin_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Лаванда 💰", "callback_data": "total_conversion"},
        {"text": "Воркеры", "callback_data": make_workers_cd(level=CURRENT_LEVEL + 1)},
        {
            "text": "Чеки",
            "callback_data": make_workers_requests_cd(level=CURRENT_LEVEL + 1),
        },
        {
            "text": "Реквизиты",
            "callback_data": make_payment_details_cd(CURRENT_LEVEL + 1),
        },
        {
            "text": "Касса",
            "callback_data": make_cashier_cd(CURRENT_LEVEL + 1),
        },
        {
            "text": "Прокси",
            "callback_data": make_proxy6_cd(CURRENT_LEVEL + 1),
        },
    ]
    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))

    return markup


async def workers_keyboard(current_page: str = "1"):
    response = requests.get(SERVER_URL + "/workers/")
    workers = response.json()
    CURRENT_LEVEL = 1
    MAX_ITEMS_PER_PAGE = 2
    MAX_PAGES = ceil(len(workers) / MAX_ITEMS_PER_PAGE)
    markup = InlineKeyboardMarkup(row_width=3)
    current_page = int(current_page)
    next_page = workers[
        (current_page * MAX_ITEMS_PER_PAGE)
        - MAX_ITEMS_PER_PAGE : current_page * MAX_ITEMS_PER_PAGE
    ]
    for worker in next_page:
        markup.row(
            InlineKeyboardButton(
                text=f"{worker.get('name')} ({worker.get('username')})",
                callback_data=make_workers_cd(
                    CURRENT_LEVEL + 1, page=current_page, worker=worker.get("id")
                ),
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=make_workers_cd(
                level=CURRENT_LEVEL,
                page=(current_page - 1) if current_page != 1 else current_page,
            ),
        )
    )
    markup.insert(
        InlineKeyboardButton(text=f"{current_page}/{MAX_PAGES}", callback_data="...")
    )

    markup.insert(
        InlineKeyboardButton(
            text=">>",
            callback_data=make_workers_cd(
                level=CURRENT_LEVEL,
                page=(current_page + 1)
                if not current_page >= MAX_PAGES
                else current_page,
            ),
        )
    )

    markup.add(
        InlineKeyboardButton(
            text="Назад", callback_data=make_workers_cd(CURRENT_LEVEL - 1)
        )
    )

    return markup


async def cashier_keyboard():
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Пополнить", "callback_data": make_cashier_cd(CURRENT_LEVEL + 1, type="deposit")},
        {"text": "Вывести", "callback_data": make_cashier_cd(CURRENT_LEVEL + 1, type="withdrawal")},
        {"text": "Назад", "callback_data": make_cashier_cd(CURRENT_LEVEL - 1)}
    ]

    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))

    return markup

async def workers_requests_keyboard(current_page: str = "1"):
    response = requests.get(SERVER_URL + "/worker/requests/")
    wrequests = response.json()
    CURRENT_LEVEL = 1
    MAX_ITEMS_PER_PAGE = 10
    MAX_PAGES = ceil(len(wrequests) / MAX_ITEMS_PER_PAGE)
    current_page = int(current_page)
    next_page = wrequests[
        (current_page * MAX_ITEMS_PER_PAGE)
        - MAX_ITEMS_PER_PAGE : current_page * MAX_ITEMS_PER_PAGE
    ]
    markup = InlineKeyboardMarkup(row_width=3)
    for wrequest in next_page:
        markup.insert(
            InlineKeyboardButton(
                text=f"{'📈' if wrequest.get('type') == 'deposit' else '📉'} {wrequest.get('amount')}",
                callback_data=make_workers_requests_cd(
                    level=CURRENT_LEVEL + 1,
                    page=current_page,
                    request=wrequest.get("id"),
                ),
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=make_workers_requests_cd(
                level=CURRENT_LEVEL,
                page=(current_page - 1) if current_page != 1 else current_page,
            ),
        )
    )
    markup.insert(
        InlineKeyboardButton(text=f"{current_page}/{MAX_PAGES}", callback_data="...")
    )

    markup.insert(
        InlineKeyboardButton(
            text=">>",
            callback_data=make_workers_requests_cd(
                level=CURRENT_LEVEL,
                page=(current_page + 1)
                if not current_page >= MAX_PAGES
                else current_page,
            ),
        )
    )

    markup.add(
        InlineKeyboardButton(
            text="Назад", callback_data=make_workers_cd(CURRENT_LEVEL - 1)
        )
    )

    return markup


async def show_worker_request_keyboard(request: str, page: str):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(
            text="Показать чек", callback_data=f"show_receipt#{request}"
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_workers_requests_cd(
                CURRENT_LEVEL - 1, page=page, request=request
            ),
        )
    )

    return markup


async def show_worker_keyboard(worker: str, page: str):
    CURRENT_LEVEL = 2
    # response = requests.get(SERVER_URL + f"/workers/{worker}")
    # worker = response.json()
    buttons = [
        {"text": "Пополнить", "callback_data": f"worker_move#refill#{worker}"},
        {"text": "Списать", "callback_data": f"worker_move#debit#{worker}"},
        {"text": "Поощрение", "callback_data": f"worker_move#reward#{worker}"},
        {"text": "Штраф", "callback_data": f"worker_move#penalty#{worker}"},
    ]
    markup = InlineKeyboardMarkup(row_width=2)
    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))
    markup.row(
        InlineKeyboardButton(text="Удалить", callback_data=f"worker_move#delete#{worker}")
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад", callback_data=make_workers_cd(CURRENT_LEVEL - 1, page=page)
        )
    )

    return markup


async def payment_details_keyboard():
    CURRENT_LEVEL = 1
    response = requests.get(SERVER_URL + "/admin/payment/details/")
    details = response.json()
    markup = InlineKeyboardMarkup(row_width=2)
    for detail in details:
        markup.row(
            InlineKeyboardButton(
                text=detail.get("name"),
                callback_data=make_payment_details_cd(
                    level=CURRENT_LEVEL + 1, detail=detail.get("id")
                ),
            )
        )
    markup.add(
        InlineKeyboardButton(text="Добавить", callback_data="add_payment_detail"),
        InlineKeyboardButton(
            text="Назад", callback_data=make_payment_details_cd(CURRENT_LEVEL - 1)
        ),
    )

    return markup


async def show_payment_detail_keyboard(detail: str):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="Удалить", callback_data=f"delete_payment_detail#{detail}"
        )
    )
    # markup.insert(
    #     InlineKeyboardButton(
    #         text="Изменить", callback_data=f"change_payment_detail#{detail}"
    #     )
    # )
    markup.insert(
        InlineKeyboardButton(
            text="Назад", callback_data=make_payment_details_cd(CURRENT_LEVEL - 1)
        )
    )

    return markup


async def payment_details_confirm_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Да", "callback_data": "add_payment_detail_confirm"},
        {"text": "Назад", "callback_data": "add_payment_detail_back#text"},
        {"text": "Отмена", "callback_data": "add_payment_detail_decline"},
    ]

    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))
    return markup
