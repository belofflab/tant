import asyncio
import sys
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from data.config import SERVER_URL

workers = [
    {
        "api_id": 27717249,
        "api_hash":"5cf673c770846a9bab792372c9bd15f4",
        "proxy": {
                "host": "217.29.62.214",
                "port": 12092,
                "username": "fy2w0z",
                "password":"NgxTcY",
                "scheme":"socks5"

            }
        }
    ]

async def handle_messages(client: Client):
    print(f"Connecting to {client.api_id}...")
    await client.start()
    me = await client.get_me()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            if me.id == dialog.chat.id:
                continue
            messages = [el async for el in client.get_chat_history(dialog.chat.id)]
            print(dialog.chat.username, "->", dialog.chat.id, "->", messages[0].date, "->", messages[-1].date)
            await asyncio.sleep(20)
            requests.post(
                url=SERVER_URL + f"/users/date/?last_activity={messages[-1].date}&first_touch={messages[0].date}",
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "id": dialog.chat.id,
                    "username": dialog.chat.username,
                    "first_name":dialog.chat.first_name,
                    "last_name": dialog.chat.last_name,
                    "worker": me.id,
                },
            )


async def main():
    for worker in workers:
        proxy_info = {
            "hostname": worker["proxy"]["host"],
            "port": worker["proxy"]["port"],
            "username": worker["proxy"]["username"],
            "password": worker["proxy"]["password"],
            "scheme": worker["proxy"]["scheme"],
        }
        client = Client(
            f'account_{worker["api_id"]}',
            api_hash=worker["api_hash"],
            api_id=worker["api_id"],
            ipv6=True,
            proxy=proxy_info
        
        )
        asyncio.create_task(handle_messages(client))

    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
