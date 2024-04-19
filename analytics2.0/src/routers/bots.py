import datetime
import ormar
import typing as t
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from src.database.models import Bot, Category, Service, BotUser
from src import schemas
from src.utils import tokenizator, files

router = APIRouter(prefix="/api/v1/bots", tags=["Боты"])


async def find_bot_worker(uid: str):
    worker_bot = await Bot.objects.filter(uid=uid).get_or_none()
    if not worker_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найден")
    return worker_bot


@router.get("/analytics")
async def get_worker_bot_anal(bot: UUID):
    s_worker_bot = await Bot.objects.get_or_none(uid=bot)
    if not s_worker_bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Бота не существует"
        )
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    users_today = await BotUser.objects.filter(
        bot=s_worker_bot, first_touch__gt=today
    ).count()
    categories = await Category.objects.filter(bot=s_worker_bot).count()
    services = await Service.objects.filter(bot=s_worker_bot).count()
    return {
        "all_users": s_worker_bot.total_users,
        "users_today": users_today,
        "all_categories": categories,
        "all_services": services,
    }


@router.get("/")
async def get_worker_bot(bot: UUID):
    s_worker_bot = await Bot.objects.get_or_none(uid=bot)
    if not s_worker_bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Бота не существует"
        )
    return {
        "bot": s_worker_bot,
    }


@router.post("/")
async def create_worker_bot(
    bot: schemas.BotCreate,
) -> schemas.WorkerRequest:
    new_bot = await Bot.objects.create(name=bot.name)
    return {"uid": new_bot.uid}


@router.get("/categories/")
async def get_services(bot: UUID, cid: int | None = None):
    worker_bot = await find_bot_worker(uid=bot)
    to_catsearch = {"bot": worker_bot}
    if cid is not None:
        to_catsearch["id"] = cid
    categories = await Category.objects.filter(**to_catsearch).all()
    services = await Service.objects.filter(bot=worker_bot, category=cid).all()
    return {"categories": categories, "services": services}


@router.delete("/categories/{cid}")
async def delete_category(cid: int):
    return await Category.objects.filter(id=cid).delete()


@router.delete("/services/{sid}")
async def delete_service(sid: int):
    return await Service.objects.filter(id=sid).delete()


@router.post("/categories/")
async def create_category(name: str, bot: UUID, cid: int | None = None):
    worker_bot = await find_bot_worker(uid=bot)
    if cid is not None:
        category = await Category.objects.get_or_none(id=cid)
        if category is not None:
            return await category.update(name=name)
    return await Category.objects.create(name=name, bot=worker_bot)


@router.post("/services/")
async def create_service(
    name: str,
    description: str,
    bot: UUID,
    sid: int | None = None,
    cid: int | None = None,
):
    worker_bot = await find_bot_worker(uid=bot)
    category = await Category.objects.get_or_none(id=cid)
    service = await Service.objects.get_or_none(id=sid)
    if service is not None:
        return await service.update(
            name=name, description=description, bot=worker_bot, category=category
        )
    return await Service.objects.create(
        name=name, description=description, bot=worker_bot, category=category
    )


@router.get("/service/{sid}")
async def get_service(bot: dict, sid: int | None = None):
    worker_bot = await find_bot_worker(uid=bot)
    return await Service.objects.filter(bot=worker_bot).get_or_none(id=sid)
