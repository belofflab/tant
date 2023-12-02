import asyncio
import sys
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from data.config import SERVER_URL
from aiogram import Bot, types

bot = Bot(token="6376476195:AAF1QYb3UQchzMcI3sQXZMxpVfpVnmES9j0")
NOTIFICATION_CHAT_ID = -4087113296
worker_request = requests.get(url=SERVER_URL + "/workers/")
if worker_request.status_code != 200:
    sys.exit(0)
workers = worker_request.json()


async def handle_messages(client: Client):
    loop = asyncio.get_event_loop()
    print(f"Connecting to {client.api_id}...")
    await client.start()
    me = await client.get_me()

    @client.on_message(filters.private)
    async def my_handler(client, message: Message):
        if not me.id == message.from_user.id:
            requests.post(
                url=SERVER_URL + "/users/?worker_name=",
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "id": message.from_user.id,
                    "username": message.from_user.username,
                    "first_name": message.from_user.first_name,
                    "last_name": message.from_user.last_name,
                    "worker": me.id,
                },
            )
        if me.id == message.from_user.id:
            json_data = {
                "sender": me.id,
                "receiver": message.chat.id,
                "text": message.text,
            }
        else:
            json_data = {
                "sender": message.chat.id,
                "receiver": me.id,
                "text": message.text,
            }
        requests.post(
            "http://127.0.0.1:9900/api/v1/messages/",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=json_data,
        )
        if message.from_user.id == 777000:
            return
        if not message.chat.type == ChatType.PRIVATE:
            return

    async def check_for_deleted_chats():
        last_chats = set()
        while True:
            current_chats = set()
            async for chat in client.get_dialogs():
                current_chats.add(chat.chat.id)
            deleted_chats = last_chats - current_chats
            if deleted_chats:
                for chat_id in deleted_chats:
                    await asyncio.sleep(0.05)
                    current_user = requests.get(
                        url=SERVER_URL + f"/users/{chat_id}"
                    ).json()
                    await bot.send_message(
                        NOTIFICATION_CHAT_ID,
                        f"Воркер @{me.username} удалил чат с @{current_user.get('username') if current_user.get('username') else current_user.get('id')}",
                        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                            types.InlineKeyboardButton(
                                text="История сообщений",
                                url=SERVER_URL + f"/messages/{me.id}/{current_user.get('id')}/"
                            )
                        )
                    )
            last_chats = current_chats
            await asyncio.sleep(3600)

    loop.create_task(check_for_deleted_chats())


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
            proxy=proxy_info,
        )
        asyncio.create_task(handle_messages(client))

    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
