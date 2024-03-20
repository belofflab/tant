import datetime
import typing as t
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from src.database.models import Bot, Worker, BotWorker
from src import schemas

router = APIRouter(prefix="/api/v1/worker/bots", tags=["Боты"])


@router.get("/{uuid}")
async def get_worker_bot(uuid: UUID):
    s_worker_bot = await Bot.objects.get_or_none(uid=uuid)
    if not s_worker_bot:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бота не существует")
    return s_worker_bot

@router.post("/")
async def create_worker_bot():
    return await Bot.objects.create()

@router.patch("/{uuid}/worker/add")
async def add_worker(uuid: UUID, worker_id: int):
    s_worker = await Worker.objects.get_or_none(user__id=worker_id)
    if not s_worker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not f")
    s_worker_bot = await Bot.objects.get_or_none(uid=uuid)
    if not s_worker_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not f")
    await BotWorker.objects.create(bot=s_worker_bot, worker=s_worker)
    return s_worker_bot

@router.get("/{uuid}/has_access")
async def has_access(uuid: UUID, worker_id: int):
    worker_bot = await Bot.objects.filter(uid=uuid).prefetch_related("workers__user").all()
    print(worker_bot)
  # return worker_id in [worker.] 
