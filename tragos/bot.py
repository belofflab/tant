import re
from datetime import datetime
import uuid
import aiohttp
from aiohttp import web
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = "6725313263:AAFAdd052QS44QSrXTpfSCBvoQVq0kcHTHU"
SERVER_URL = "https://tant.belofflab.com/tragos/"
WEB_APP_PORT = 6677
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

cookies = {
    'sNdOIy': 'qkeUJMPwIEAoCnaFfOruWBpyYsSTcZ',
    'cookie_id': '524409947cookie_id6641b9c8a0e04',
    'host_name': 'tragos.ru',
    '_ga': 'GA1.1.1249311112.1715583433',
    '_ym_uid': '1715583276790850989',
    '_ym_d': '1715583434',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'PHPSESSID': '575bf1152d54d87f6a4cf32e38f4dfba',
    'qkeUJMPwIEAoCnaFfOruWBpyYsSTcZ': 'bde7538c5cbc3366adb3d110ccd36209-1715583465-1715583459',
    '_ga_17NFE2NVJR': 'GS1.1.1715583433.1.1.1715583951.0.0.0',
    'sNdOIy_hits': '31',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://tragos.ru',
    'Referer': 'https://tragos.ru/alignment-for-the-year/?day=4&month=6&year=2018&age=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


async def get_astrology_report(date_of_birth: datetime, age: str = ""):
    data = {
        "task": "alignment-for-the-year",
        "day": date_of_birth.day,
        "month": date_of_birth.month,
        "year": date_of_birth.year,
        "age": age,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://tragos.ru/tragos_ajax", headers=headers, data=data, cookies=cookies
        ) as response:
            html_content = await response.text()

            soup = BeautifulSoup(html_content, "lxml")
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


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(
        "Привет, я бот Лабиринта Осознанности! Пришлите дату рождения в формате \n\n10.10.2020 18 или 10.10.2020"
    )


@dp.message_handler(regexp=r"(\d{2}\.\d{2}\.\d{4})\s*(\d{1,2})?")
async def handle_date(message: types.Message):
    date_of_birth = re.search(r"(\d{2}\.\d{2}\.\d{4})\s*(\d{1,2})?", message.text)

    if date_of_birth:
        birth_time = date_of_birth.group(2) if date_of_birth.group(2) else ""
        date_of_birth = datetime.strptime(date_of_birth.group(1), "%d.%m.%Y")
        report_content = await get_astrology_report(date_of_birth, age=birth_time)

        report_filename = f"media/{uuid.uuid4()}.html"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(f"<div id='result'>{report_content}</div>")

        await message.reply(
            f"Ващ отчет: {report_filename}",
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton(
                    text=f"Отчет {date_of_birth}",
                    url=SERVER_URL + report_filename,
                )
            ),
        )


async def on_startup(dp):
    app = web.Application()
    app.router.add_static("/media", "media", name="media")
    app.router.add_routes([web.get("/", lambda r: web.Response(text="Hello, world!"))])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", WEB_APP_PORT)
    await site.start()

if __name__ == "__main__":
    # executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

