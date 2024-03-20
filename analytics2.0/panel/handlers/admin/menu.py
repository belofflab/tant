import requests

from aiogram import types
from loader import dp
from data.config import SERVER_URL

@dp.message_handler(commands='admin')
async def admin(message: types.Message) -> None:
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "Посмотреть",
            web_app=types.WebAppInfo(url=f"""{SERVER_URL}/analytics/info/""")
        )
    )
    await message.answer(text="Вы можете посмотреть аналитику по ссылке ниже", reply_markup=markup)