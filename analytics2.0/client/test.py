import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from data.config import SERVER_URL
from aiogram import Bot

bot = Bot(token="6376476195:AAF1QYb3UQchzMcI3sQXZMxpVfpVnmES9j0")
NOTIFICATION_CHAT_ID = -4087113296
workers = [{"api_id": 9263799, "api_hash":"2026ebfabef0da1b38b18b12be0e64ca"}]


async def handle_messages(client: Client):
    loop = asyncio.get_event_loop()
    print(f"Connecting to {client.api_id}...")
    await client.start()
    me = await client.get_me()

    @client.on_message(filters.private)
    async def my_handler(client, message: Message):
        if me.id == message.from_user.id:
            return
        if not message.chat.type == ChatType.PRIVATE:
            return 
        requests.post(
            url=SERVER_URL + "/users/",
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
                    # print(f"Воркер {me.id} удалил чат с {chat_id}")
                    await bot.send_message(NOTIFICATION_CHAT_ID, f"Воркер {me.id} удалил чат с {chat_id}")
            last_chats = current_chats
            await asyncio.sleep(3600)
    loop.create_task(check_for_deleted_chats())


async def main():
    for worker in workers:
        client = Client(
            f'account_{worker["api_id"]}',
            api_hash=worker["api_hash"],
            api_id=worker["api_id"],
        )
        asyncio.create_task(handle_messages(client))

    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
