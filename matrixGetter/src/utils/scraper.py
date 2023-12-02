import asyncio
from typing import Optional

from arsenic import get_session
from arsenic.browsers import Chrome
from arsenic.services import Remote
from arsenic.session import Session

from bs4 import BeautifulSoup


async def make_screenshot(session: Session, url: str) -> Optional[dict]:
    await session.get(url)

    result = await session.get_element("#result")
    screenshot_data = await result.get_screenshot()
    page_source = await session.get_page_source()
    html = BeautifulSoup(page_source, "lxml")
    rows = html.select("div.result__row > div.result__item")

    matrix = {}

    for row in rows:
        name = row.select_one("h4").text.strip().lower()
        value = row.select_one("p").text.strip().lower()
        matrix[name] = value


    return screenshot_data, matrix


async def start_scrape(url: str) -> dict:
    async with get_session(
        Remote(url="http://194.190.152.23:4444/wd/hub"),
        Chrome(),
    ) as session:
        return await make_screenshot(session, url=url)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print(
        loop.run_until_complete(
            start_scrape(url="https://matrix.belofflab.com/?date=24.09.2005")
        )
    )
