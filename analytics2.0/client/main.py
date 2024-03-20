import asyncio
import sys
from uuid import uuid4
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from data.config import SERVER_URL, BASE_DIR
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

    async def download_voice(client: Client, message: Message):
        file_extension = message.voice.mime_type.split("/")[-1]
        file_path = f"media/voices/{uuid4()}.{file_extension}"
        await client.download_media(message, file_name=f"{BASE_DIR.parent}/{file_path}")
        return file_path

    async def download_photo(client: Client, message: Message):
        file_path = f"media/photos/{uuid4()}.png"
        await client.download_media(message, file_name=f"{BASE_DIR.parent}/{file_path}")
        return file_path

    async def proceed_message(client: Client, message: Message):
        if message.text:
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
        elif message.caption:
            photo_path = await download_photo(client=client, message=message)
            if me.id == message.from_user.id:
                json_data = {
                    "sender": me.id,
                    "receiver": message.chat.id,
                    "text": message.caption,
                    "photo": photo_path,
                }
            else:
                json_data = {
                    "sender": message.chat.id,
                    "receiver": me.id,
                    "text": message.caption,
                    "photo": photo_path,
                }
        elif message.photo:
            photo_path = await download_photo(client=client, message=message)
            if me.id == message.from_user.id:
                json_data = {
                    "sender": me.id,
                    "receiver": message.chat.id,
                    "photo": photo_path,
                }
            else:
                json_data = {
                    "sender": message.chat.id,
                    "receiver": me.id,
                    "photo": photo_path,
                }
        elif message.voice:
            voice_path = await download_voice(client=client, message=message)
            if me.id == message.from_user.id:
                json_data = {
                    "sender": me.id,
                    "receiver": message.chat.id,
                    "voice": voice_path,
                }
            else:
                json_data = {
                    "sender": message.chat.id,
                    "receiver": me.id,
                    "voice": voice_path,
                }
        else:
            return
        requests.post(
            "http://127.0.0.1:9900/api/v1/messages/",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=json_data,
        )

    @client.on_message(filters.private)
    async def my_handler(client, message: Message):
        if message.from_user.id == 777000:
            return
        if not message.chat.type == ChatType.PRIVATE:
            return
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
        loop.create_task(proceed_message(client, message))

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
                                url=SERVER_URL
                                + f"/messages/{me.id}/{current_user.get('id')}/",
                            )
                        ),
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
