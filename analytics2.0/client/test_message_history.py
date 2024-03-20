import asyncio
import sys
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from data.config import SERVER_URL
from aiogram import Bot

bot = Bot(token="6376476195:AAF1QYb3UQchzMcI3sQXZMxpVfpVnmES9j0")
NOTIFICATION_CHAT_ID = -4087113296
workers = [{"api_id": 9263799, "api_hash": "2026ebfabef0da1b38b18b12be0e64ca"}]


async def handle_messages(client: Client):
    print(f"Connecting to {client.api_id}...")
    await client.start()
    me = await client.get_me()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.PRIVATE:
            messages = [el async for el in client.get_chat_history(dialog.chat.id)]
            requests.post(
                url=f"http://127.0.0.1:9900/users/date/?last_activity={messages[-1].date}&first_touch={messages[0].date}",
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "id": dialog.chat.id,
                    "username": dialog.chat.username,
                    "first_name": dialog.chat.first_name,
                    "last_name": dialog.chat.last_name,
                    "worker": me.id,
                }
            )
            for message in messages:
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
                    requests.post(
                        "http://127.0.0.1:9900/api/v1/messages/",
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                        },
                        json=json_data,
                    )



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
