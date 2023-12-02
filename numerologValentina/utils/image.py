from loader import bot
from data.config import BASE_DIR
from uuid import uuid4
from aiogram import types

async def save(message: types.Message):
    destination = f'media/{uuid4()}.png'
    await message.photo[-1].download(destination_file=BASE_DIR / destination)

    return destination