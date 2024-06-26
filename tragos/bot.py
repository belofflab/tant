import asyncio
import re
import requests
from datetime import datetime
import uuid
from aiohttp import web
from aiogram.filters import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types

API_TOKEN = "6725313263:AAFAdd052QS44QSrXTpfSCBvoQVq0kcHTHU"
SERVER_URL = "https://tant.belofflab.com/tragos/"
WEB_APP_PORT = 6677
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()


def get_astrology_report(date_of_birth: datetime, age: str = ""):
    cookies = {
        'sNdOIy': 'tmnBfKRYHLkbGrZVOwWCePUJTzoapy',
        'cookie_id': '1178259313cookie_id663b27046e0d4',
        '_ga': 'GA1.1.1894583234.1715152644',
        '_ym_uid': '171515264486072643',
        '_ym_d': '1715152648',
        'PHPSESSID': '59fce89f782890ff839ecf98c46f8bcc',
        'host_name': 'tragos.ru',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        'tmnBfKRYHLkbGrZVOwWCePUJTzoapy': '19e9473fd44f06e5f51ed124f316ad6e-1717950887-1717950883',
        'sNdOIy_hits': '38',
        '_ga_17NFE2NVJR': 'GS1.1.1717950469.2.1.1717950960.0.0.0',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://tragos.ru',
        'Referer': 'https://tragos.ru/alignment-for-the-year/?day=4&month=6&year=2018&age=6',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        "task": "alignment-for-the-year",
        "day": date_of_birth.day,
        "month": date_of_birth.month,
        "year": date_of_birth.year,
        "age": age,
    }
    response = requests.post('https://tragos.ru/tragos_ajax', cookies=cookies, headers=headers, data=data)
    soup = BeautifulSoup(response.text, "lxml")
    style = soup.new_tag("style")
    styles = open("./styles.css", "r").read()
    style.string = styles
    soup.insert(2, style)
    soup.select_one("body > div").clear()

    for element in soup.select('img[src="/images/question.png"]'):
        element.attrs.update({"src": "https://tragos.ru/images/question.png"})

    for element in soup.select("a"):
        href = element.attrs.get("href")
        if "#" in href:
            continue
        elif "https://tragos.ru/" in href or href.endswith(".html"):
            element.attrs.clear()

    soup.select("script").clear()

    return str(soup)

@router.message(Command("start"))
async def start(message: types.Message):
    await message.reply(
        "Привет, я бот Лабиринта Осознанности! Пришлите дату рождения в формате \n\n10.10.2020 18 или 10.10.2020"
    )


@router.message(F.text.regexp(r"(\d{2}\.\d{2}\.\d{4})\s*(\d{1,2})?"))
async def handle_date(message: types.Message):
    date_of_birth = re.search(r"(\d{2}\.\d{2}\.\d{4})\s*(\d{1,2})?", message.text)

    if date_of_birth:
        birth_time = date_of_birth.group(2) if date_of_birth.group(2) else ""
        date_of_birth = datetime.strptime(date_of_birth.group(1), "%d.%m.%Y")
        report_content = get_astrology_report(date_of_birth, age=birth_time)

        report_filename = f"media/{uuid.uuid4()}.html"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(f"<div id='result'>{report_content}</div>")
        keyboard = InlineKeyboardBuilder()
        keyboard.row(types.InlineKeyboardButton(
                    text=f"Отчет {date_of_birth}",
                    url=SERVER_URL + report_filename,
                ))
        await message.reply(
            f"Ващ отчет: {report_filename}",
            reply_markup=keyboard.as_markup()
        )


async def on_startup(dp):
    dp.include_router(router)
    app = web.Application()
    app.router.add_static("/media", "media", name="media")
    app.router.add_routes([web.get("/", lambda r: web.Response(text="Hello, world!"))])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", WEB_APP_PORT)
    await site.start()

async def main():
    await on_startup(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

