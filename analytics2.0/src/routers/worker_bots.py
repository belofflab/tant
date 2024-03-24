import datetime
import ormar
import typing as t
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from src.database.models import Bot, Worker, BotWorker, Category, Service, BotUser
from src import schemas
from src.middlewares.bearers.bot import BotBearer
from src.utils import tokenizator, files

router = APIRouter(prefix="/api/v1/worker/bots", tags=["Боты"])

async def find_bot_worker(uid: str):
    worker_bot = await Bot.objects.filter(uid=uid).get_or_none()
    if not worker_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найден")
    return worker_bot

# @router.get("/")
# async def get_worker_bots():
#     return await Bot.objects.all()

@router.get("/analytics")
async def get_worker_bot_anal(bot: dict = Depends(BotBearer())):
    s_worker_bot = await Bot.objects.get_or_none(uid=UUID(bot["uuid"]))
    if not s_worker_bot:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бота не существует")
    all_users = await BotUser.objects.filter(bot=s_worker_bot).count()
    today = datetime.datetime.now() - datetime.timedelta(days=1)
    users_today = await BotUser.objects.filter(bot=s_worker_bot,first_touch__gt=today).count()
    categories = await Category.objects.filter(bot=s_worker_bot).count() 
    services = await Service.objects.filter(bot=s_worker_bot).count() 
    return {
        "all_users": all_users,
        "users_today": users_today,
        "all_categories": categories,
        "all_services": services
    }

@router.get("/")
async def get_worker_bot(bot: dict = Depends(BotBearer())):
    s_worker_bot = await Bot.objects.get_or_none(uid=UUID(bot["uuid"]))
    s_workers = await BotWorker.objects.filter(bot=s_worker_bot).prefetch_related("worker__user").all()
    if not s_worker_bot:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бота не существует")
    return {
        "bot": s_worker_bot,
        "workers": [worker_bot.worker for worker_bot in s_workers]
    }


@router.post("/")
async def create_worker_bot(
    bot: schemas.BotCreate = Depends(),
    main_photo: t.Optional[UploadFile] = File(default=None),
) -> schemas.WorkerRequest:
    main_photo_path = None
    if main_photo:
        main_photo_path = files.create(file=main_photo, upath="bots")

    new_bot =  await Bot.objects.create(
        main_photo=main_photo_path, 
        main_description=bot.main_description, 
        service_description=bot.service_description
    )

    return {"access_token": tokenizator.create({"uuid": str(new_bot.uid), "workers": []})}

@router.patch("/worker/add")
async def add_worker(wid: int, bot: dict = Depends(BotBearer())):
    s_worker = await Worker.objects.get_or_none(user__id=wid)
    if not s_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not f")
    s_worker_bot = await Bot.objects.get_or_none(uid=UUID(bot["uuid"]))
    if not s_worker_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not f")
    new_worker = await BotWorker.objects.create(bot=s_worker_bot, worker=s_worker)
    bot["workers"].append(new_worker.id) 
    return {"access_token": tokenizator.create({"uuid": str(s_worker_bot.uid), "workers": bot["workers"]})}


@router.post("/authorize/{uuid}")
async def authorize_bot(uuid: UUID):
    worker_bot = await Bot.objects.filter(uid=uuid).get_or_none()
    workers = await BotWorker.objects.filter(bot=worker_bot).all()
    if worker_bot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="не найден")
    return {"access_token": tokenizator.create({"uuid": str(worker_bot.uid), "workers": [worker.id for worker in workers]})}

@router.get("/categories/")
async def get_services(cid: int | None = None, bot: dict = Depends(BotBearer())):
    worker_bot = await find_bot_worker(uid=UUID(bot["uuid"]))
    to_catsearch = {"bot": worker_bot}
    if cid is not None:
        to_catsearch["id"] = cid
    categories = await Category.objects.filter(**to_catsearch).all()
    services = await Service.objects.filter(bot=worker_bot, category=cid).all()
    return {
        "categories": categories,
        "services": services
    }

@router.delete("/categories/{cid}")
async def delete_category(cid: int, bot: dict = Depends(BotBearer())):
    return await Category.objects.filter(id=cid).delete()


@router.delete("/services/{sid}")
async def delete_service(sid: int, bot: dict = Depends(BotBearer())):
    return await Service.objects.filter(id=sid).delete()

@router.post("/categories/")
async def create_category(name: str, cid: int | None = None, bot: dict = Depends(BotBearer())):
    worker_bot = await find_bot_worker(uid=UUID(bot["uuid"]))
    if cid is not None:
        category = await Category.objects.get_or_none(id=cid)
        if category is not None:
            return await category.update(name=name)
    return await Category.objects.create(name=name, bot=worker_bot)

@router.post("/services/")
async def create_service(name: str, description: str, sid: int | None = None, cid: int | None = None, bot: dict = Depends(BotBearer())):
    worker_bot = await find_bot_worker(uid=UUID(bot["uuid"]))
    category = await Category.objects.get_or_none(id=cid)
    service = await Service.objects.get_or_none(id=sid)
    if service is not None:
        return await service.update(name=name, description=description,bot=worker_bot, category=category)
    return await Service.objects.create(name=name, description=description,bot=worker_bot, category=category)


@router.get("/service/{sid}")
async def get_service(sid: int | None = None, bot: dict = Depends(BotBearer())):
    worker_bot = await find_bot_worker(uid=UUID(bot["uuid"]))
    return await Service.objects.filter(bot=worker_bot).get_or_none(id=sid)
