import requests 
from data.config import SERVER_URL
from math import ceil
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

uworkers_requests_cd = CallbackData("show_uworkers_requests", "level", "page", "request")
user_payment_details_cd = CallbackData("show_user_payment_details", "level", "detail")


def make_uworkers_requests_cd(level, page="1", request="0"):
    return uworkers_requests_cd.new(level=level, page=page, request=request)

def make_user_payment_details_cd(level, detail="0"):
    return user_payment_details_cd.new(level=level, detail=detail)




async def worker_menu_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        {"text": "Отправить чек", "callback_data": "proceed_receipt"},
        {"text": "Запросить выплату", "callback_data": "proceed_payout"},
        {"text": "Чеки", "callback_data": make_uworkers_requests_cd(CURRENT_LEVEL + 1)},
        {"text": "Реквизиты", "callback_data": make_user_payment_details_cd(CURRENT_LEVEL + 1)},
    ]

    for button in buttons:
        markup.insert(
            InlineKeyboardButton(**button)
        )

    return markup

async def payment_details_keyboard(user_id: int):
    CURRENT_LEVEL = 1
    response = requests.get(SERVER_URL + f"/users/{user_id}/payment/details/")
    details = response.json()
    markup = InlineKeyboardMarkup(row_width=2)
    for detail in details:
        markup.row(
            InlineKeyboardButton(
                text=detail.get("name"),
                callback_data=make_user_payment_details_cd(
                    level=CURRENT_LEVEL + 1, detail=detail.get("id")
                ),
            )
        )
    markup.add(
        InlineKeyboardButton(text="Добавить", callback_data="add_user_payment_detail"),
        InlineKeyboardButton(
            text="Назад", callback_data=make_user_payment_details_cd(CURRENT_LEVEL - 1)
        ),
    )

    return markup


async def show_payment_detail_keyboard(detail: str):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="Удалить", callback_data=f"delete_user_payment_detail#{detail}"
        )
    )
    # markup.insert(
    #     InlineKeyboardButton(
    #         text="Изменить", callback_data=f"change_payment_detail#{detail}"
    #     )
    # )
    markup.insert(
        InlineKeyboardButton(
            text="Назад", callback_data=make_user_payment_details_cd(CURRENT_LEVEL - 1)
        )
    )

    return markup


async def payment_details_confirm_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Да", "callback_data": "add_user_payment_detail_confirm"},
        {"text": "Назад", "callback_data": "add_user_payment_detail_back#text"},
        {"text": "Отмена", "callback_data": "add_user_payment_detail_decline"},
    ]

    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))
    return markup



async def workers_requests_keyboard(worker: int, current_page: str = "1"):
    response = requests.get(SERVER_URL + f"/worker/requests/{worker}/")
    wrequests = response.json()
    CURRENT_LEVEL = 1
    MAX_ITEMS_PER_PAGE = 5
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
                callback_data=make_uworkers_requests_cd(
                    level=CURRENT_LEVEL + 1,
                    page=current_page,
                    request=wrequest.get("id"),
                ),
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="<<",
            callback_data=make_uworkers_requests_cd(
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
            callback_data=make_uworkers_requests_cd(
                level=CURRENT_LEVEL,
                page=(current_page + 1)
                if not current_page >= MAX_PAGES
                else current_page,
            ),
        )
    )

    markup.add(
        InlineKeyboardButton(
            text="Назад", callback_data=make_uworkers_requests_cd(CURRENT_LEVEL - 1)
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
            callback_data=make_uworkers_requests_cd(
                CURRENT_LEVEL - 1, page=page, request=request
            ),
        )
    )

    return markup



async def worker_receipt_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        {"text": "Назад", "callback_data": "receipt_back"},
    ]
    for button in buttons:
        markup.insert(
            InlineKeyboardButton(**button)
        )

    return markup

async def worker_payout_keyboard(all_sum = True):
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        {"text": "Вывести всю сумму", "callback_data": "payout_all"},
        {"text": "Назад", "callback_data": "payout_back"},
    ]
    for idx, button in enumerate(buttons):
        if not all_sum:
            if idx == 0:
                continue
        markup.insert(
            InlineKeyboardButton(**button)
        )

    return markup

async def confirm_deposit_request_keyboard(request_id: int):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Подвердить ✅", "callback_data": f"deposit_request_confirm#{request_id}"},
        {"text": "Отклонить ❌", "callback_data": f"deposit_request_decline#{request_id}"},
    ]
    for button in buttons:
        markup.insert(
            InlineKeyboardButton(**button)
        )

    return markup

async def confirm_withdrawal_request_keyboard(request_id: int):
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        {"text": "Подвердить ✅", "callback_data": f"withdrawal_request_confirm#{request_id}"},
        {"text": "Отклонить ❌", "callback_data": f"withdrawal_request_decline#{request_id}"},
    ]
    for button in buttons:
        markup.insert(
            InlineKeyboardButton(**button)
        )

    return markup

async def chooose_payment_detail_keyboard(user_id: int, amount: int):
    response = requests.get(
        SERVER_URL + f"/users/{user_id}/payment/details/"
    )

    payment_details = response.json()
    markup = InlineKeyboardMarkup(row_width=1)

    for payment_detail in payment_details:
        markup.row(
            InlineKeyboardButton(
                text=payment_detail.get("name"),
                callback_data=f"payment_detail#choose#{amount}#-#{payment_detail.get('id')}"
            )
        )

    markup.row(
        InlineKeyboardButton(
            text="Добавить",
            callback_data=f"payment_detail#add#{amount}#-#-"
        )
    )

    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"payment_detail#back#{amount}#-#-"
        )
    )

    return markup