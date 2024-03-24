import datetime
import typing as t

from fastapi import APIRouter, HTTPException, status
from src.database.models import User, Worker, Transition, UserPaymentDetail, Bot, BotUser
from src import schemas

router = APIRouter(prefix="/api/v1/users", tags=["Пользователи"])


@router.get("/{id}")
async def get_user(id: int):
    return await User.objects.get(id=id)


@router.get("/")
async def get_users():
    return await User.objects.all()


@router.post("/")
async def get_or_create_user(user: schemas.UserCreate) -> schemas.User:
    s_user = await User.objects.get_or_none(id=user.id)
    s_worker_bot = await Bot.objects.get_or_none(uid=user.worker_bot)

    if not s_worker_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бот не был найден в базе",
        )

    if not s_user:
        new_user = await User.objects.create(
            id=user.id,
            full_name=user.full_name,
            username=user.username,
        )
        await BotUser.objects.create(bot=s_worker_bot, user=s_user)
        return new_user
    to_update = {"last_activity": datetime.datetime.now()}
    if user.full_name != s_user.full_name:
        to_update["full_name"] = user.full_name
    if user.username != s_user.username:
        to_update["username"] = user.username
    await s_user.update(**to_update)

    return s_user

@router.get("/{user}/payment/details/")
async def get_user_payment_details(user: int) -> schemas.UserPaymentDetail:
    s_user = await User.objects.get_or_none(id=user)
    return await UserPaymentDetail.objects.filter(user=s_user).all()


@router.get("/payment/details/")
async def get_user_payment_detail(id: int) -> schemas.UserPaymentDetail:
    return await UserPaymentDetail.objects.get_or_none(id=id)


@router.post("/payment/details/")
async def create_payment_details(
    detail: schemas.UserPaymentDetailCreate,
) -> schemas.UserPaymentDetail:
    return await UserPaymentDetail.objects.create(
        name=detail.name,
        user=await User.objects.get_or_none(id=detail.user),
        text=detail.text,
    )


@router.delete("/payment/details/{detail}")
async def delete_payment_detail(detail: int) -> None:
    await UserPaymentDetail.objects.filter(id=detail).delete()
