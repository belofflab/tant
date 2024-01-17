import asyncio
import re 
from aiogram import exceptions
from loader import bot
from database import models

from data.config import BASE_DIR

from aiogram.types import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup, InputFile


def detect_url(button: str) -> str:
    button_info = button.split('/')
    if not len(button_info)> 1:
        return {'text': None, 'callback_data': None} 
    if 'http' in button_info[1]:
        return {'text': button_info[0], 'url': button_info[-1]}
    return {'text': button_info[0], 'callback_data': button_info[1]}

def fast_proceed_buttons(buttons: str):
    if buttons is None:
        return None
    markup = InlineKeyboardMarkup()
    for button in buttons.splitlines():
        if len(button.split('/')) > 1:
            markup.insert(
                InlineKeyboardButton(
                    **detect_url(button=button)
                )
            )

    return markup

async def custom_edit_message(chat_id, photo: str, text: str, buttons: str, **kwargs):
        new_text = text
        if photo is not None:
            new_text = text + "\n\nФото успешно изменено!"
            # await bot.edit_message_media(
            #     media=InputMediaPhoto(media=InputFile(BASE_DIR / photo)),
            #     chat_id=chat_id,
            #     **kwargs
            # )
        message = await bot.edit_message_text(
            chat_id=chat_id,
            text=new_text,
            reply_markup=fast_proceed_buttons(buttons=buttons),
            **kwargs
        )

        return message
async def custom_send_message(chat_id, photo: str, text: str, buttons: str):
    if photo is not None:
        message = await bot.send_photo(
            photo=InputFile(BASE_DIR / photo),
            chat_id=chat_id,
            caption=text,
            reply_markup=fast_proceed_buttons(buttons=buttons),
        )
    else:
        message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=fast_proceed_buttons(buttons=buttons),
        )
    return message

async def go(photo: str, text: str, buttons: str, users: list):
    for user in users:
        await asyncio.sleep(0.04)
        try:
            await custom_send_message(
                chat_id=user.idx,
                photo=photo,
                text=text,
                buttons=buttons
            )
        # except exceptions.BotBlocked:
        #     await models.User.update.values(is_active=False).where(
        #         models.User.idx == user.idx
        #     ).gino.status()
        except Exception as ex:
            print('Unknown error', ex)