from aiogram import types
from database import models
from keyboards.user import inline
from loader import dp
from data.config import BASE_DIR, WORKER_PHOTO
from .menu import start


async def list_service_types(callback: types.CallbackQuery, worker, **kwargs) -> None:
    service_types = await models.ServiceType.query.gino.all()
    services = await models.Service.query.where(
        models.Service.type == None
    ).gino.all()
    markup = await inline.service_types_keyboard(worker=worker, service_types=service_types, services=services)
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"

    await callback.message.edit_media(media=types.InputMediaPhoto(
                media=types.InputFile(WORKER_PHOTO),caption=text), reply_markup=markup)


async def list_services(
    callback: types.CallbackQuery, service_type: str, worker: str, **kwargs
) -> None:
    service_type = await models.ServiceType.query.where(models.ServiceType.idx == int(service_type)).gino.first()
    if not service_type:
        return
    services = await models.Service.query.where(
        models.Service.type == service_type.idx
    ).gino.all()
    markup = await inline.services_keyboard(service_type, worker, services)
    text = "Чтобы узнать подробнее о каждом виде консультации, нажмите на соответствующую кнопку 👇"
    if service_type.photo:
        await callback.message.edit_media(media=types.InputMediaPhoto(media=types.InputFile(BASE_DIR / service_type.photo), caption=text), reply_markup=markup)
    else:
        await callback.message.edit_caption(caption=text, reply_markup=markup)

async def show_service(
    callback: types.CallbackQuery, service_type: str, service: str, worker: str
) -> None:
    markup = await inline.show_service(
        service=service, service_type=service_type, worker=worker
    )
    q_service = await models.Service.query.where(
        models.Service.idx == int(service)
    ).gino.first()

    await callback.message.edit_caption(
        caption=f"""
{q_service.description.format(worker=worker)}
{f"Стоимость: <i>{int(q_service.amount)}₽</i> " if  q_service.amount > 0 else ''}
""",
        reply_markup=markup,
    )


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
