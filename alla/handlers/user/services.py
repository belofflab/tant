from aiogram import types
from keyboards.user import inline
from loader import dp, analytics
from data.config import BASE_DIR, WORKER_PHOTO
from .menu import start


async def list_service_types(callback: types.CallbackQuery, worker, **kwargs) -> None:
    data = analytics.send_request("/worker/bots/categories/")
    markup = await inline.service_types_keyboard(worker=worker, service_types=data["categories"], services=data["services"])
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"

    await callback.message.edit_media(media=types.InputMediaPhoto(
                media=types.InputFile(WORKER_PHOTO),caption=text), reply_markup=markup)


async def list_services(
    callback: types.CallbackQuery, service_type: str, worker: str, **kwargs
) -> None:
    data = analytics.send_request("/worker/bots/categories/?cid=" + service_type)
    markup = await inline.services_keyboard(service_type, worker,services=data["services"])
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"
    if data["categories"][0]["photo"]:
        await callback.message.edit_media(media=types.InputMediaPhoto(media=types.InputFile(BASE_DIR / service_type[0]["photo"]), caption=text), reply_markup=markup)
    else:
        await callback.message.edit_caption(caption=text, reply_markup=markup)

async def show_service(
    callback: types.CallbackQuery, service_type: str, service: str, worker: str
) -> None:
    markup = await inline.show_service(
        service=service, service_type=service_type, worker=worker
    )
    data = analytics.send_request(f"/worker/bots/service/{service}")
    await callback.message.edit_caption(
        caption=data["description"],
        reply_markup=markup,
    )
    if data["photo"]:
        await callback.message.edit_media(media=types.InputMediaPhoto(media=types.InputFile(BASE_DIR / data["photo"]), caption=data["description"]), reply_markup=markup)
    else:
        await callback.message.edit_caption(caption=data["description"], reply_markup=markup)


@dp.callback_query_handler(inline.service_cd.filter())
async def service_navigate(callback: types.CallbackQuery, callback_data: dict) -> None:
    level = callback_data.get("level")
    service_type = callback_data.get("type")
    service = callback_data.get("service")
    worker = callback_data.get("worker")

    levels = {
        "0": start,
        "1": list_service_types,
        "2": list_services,
        "3": show_service,
    }

    current_level_function = levels[level]

    await current_level_function(
        callback, service=service, service_type=service_type, worker=worker
    )
