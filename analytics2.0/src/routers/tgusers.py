import datetime
import typing as t
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from src.database.models import TGUser, Bot, BotUser
from src import schemas

router = APIRouter(prefix="/api/v1/tg/users", tags=["Телеграмм пользователи"])


async def find_bot(uid: str):
    worker_bot = await Bot.objects.filter(uid=uid).get_or_none()
    if not worker_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найден")
    return worker_bot


@router.get("/")
async def get_tgusers(bot_uid: UUID):
    bot = await find_bot(uid=bot_uid)

    return await BotUser.objects.filter(bot=bot).all()


@router.post("/")
async def get_or_create_tguser(user: schemas.TGUserCreate) -> schemas.TGUserCreate:
    bot = await find_bot(uid=user.worker_bot)
    s_user, _ = await TGUser.objects.get_or_create(
        id=user.id, username=user.username, full_name=user.full_name
    )
    bot_user = await BotUser.objects.filter(bot=bot, tguser=s_user).get_or_none()
    if bot_user is None:
        await bot.update(total_users=bot.total_users + 1)
        bot_user = await BotUser.objects.create(bot=bot, tguser=s_user)
    else:
        to_update_user = {}
        if user.full_name != s_user.full_name:
            to_update_user["full_name"] = user.full_name
        if user.username != s_user.username:
            to_update_user["username"] = user.username
        if len(to_update_user) > 0:
            await s_user.update(**to_update_user)
        await bot_user.update(
            **{"last_activity": datetime.datetime.now(), "is_active": True}
        )
    return {"user": user, "bot_user": bot_user}


@router.patch("/{id}/switch_active")
async def set_active_tg_user(tguser: schemas.TGUserPatch):
    bot = await find_bot(uid=tguser.worker_bot)
    bot_user = await BotUser.objects.filter(bot=bot.id, tguser=tguser.id).get_or_none()
    if bot_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="404",
        )
    return await bot_user.update(is_active=not bot_user.is_active)
