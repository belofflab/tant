import requests
from aiogram import types
from loader import dp, proxy6
from data.config import SERVER_URL
from filters.is_admin import IsAdmin
from aiogram.dispatcher import FSMContext
from keyboards.admin import inline
from .menu import admin

def get_worker_proxies():
    proxies = proxy6.getproxy().json()
    workers = requests.get(SERVER_URL + "/workers/").json()
    combined_info = {}
    balance = proxies["balance"]
    for worker in workers:
        for key,value in proxies["list"].items():
            if worker["proxy"]["username"] == value["user"] and worker["proxy"]["password"] == value["pass"]:
                combined_info[key] = {
                    "name": worker["name"],
                    "host": value["host"],
                    "user": value["user"],
                    "pass": value["pass"],
                    "date": value["date"],
                    "date_end": value["date_end"],
                    "active": value["active"]
                }
    return balance, combined_info


async def list_proxies(callback: types.CallbackQuery, **kwargs):
    balance, combined_info = get_worker_proxies()
    await callback.message.edit_caption(
        f"""
<b>Баланс</b> <a href="https://proxy6.net">proxy6</a>: ${balance}
""",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            *[
                types.InlineKeyboardButton(
                    text=f'{value["name"]} {"✅" if  value["active"] == "1" else "❌"}',
                    callback_data=inline.make_proxy6_cd(level=2, proxy=key),
                )
                for key, value in combined_info.items()
            ],
            types.InlineKeyboardButton(text="Назад", callback_data=inline.make_proxy6_cd(level=0))
        ),
    )

async def show_proxy(callback: types.CallbackQuery, proxy: str):
    balance, combined_info = get_worker_proxies()
    await callback.message.edit_caption(
        f"""
Пользователь: <b>{combined_info[proxy]["name"]}</b>

IP: <code>{combined_info[proxy]["host"]}</code>
Логин: <code>{combined_info[proxy]["user"]}</code>
Пароль: <code>{combined_info[proxy]["pass"]}</code>

Дата создания: <b>{combined_info[proxy]["date"]}</b>
Дата окончания: <b>{combined_info[proxy]["date_end"]}</b>

Активен: {'✅' if  combined_info[proxy]["active"] == '1' else '❌'}
""",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(text="Назад", callback_data=inline.make_proxy6_cd(level=1))
        ),
    )


@dp.callback_query_handler(IsAdmin(), inline.proxy6_cd.filter())
async def proxy6_navigate(
    callback: types.CallbackQuery, callback_data: dict
) -> None:
    level = callback_data.get("level")
    proxy = callback_data.get("proxy")

    levels = {
        "0": admin,
        "1": list_proxies,
        "2": show_proxy
    }

    current_level_function = levels[level]

    await current_level_function(callback, proxy=proxy)
