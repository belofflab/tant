import datetime
import typing as t

from fastapi import APIRouter, HTTPException, status
from src.database.models import User, Worker, Transition, UserPaymentDetail
from src import schemas

router = APIRouter(prefix="/api/v1/users", tags=["Пользователи"])


@router.get("/{id}")
async def get_user(id: int):
    return await User.objects.get(id=id)

@router.get("/")
async def get_users():
    return await User.objects.prefetch_related("worker").all()

@router.post("/")
async def get_or_create_user(
    worker_name: t.Optional[str], user: schemas.UserCreate
) -> schemas.User:
    s_user = await User.objects.get_or_none(id=user.id)
    s_worker = await Worker.objects.get_or_none(id=user.worker)

    if not s_worker:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данный работник не был найден",
        )

    if not s_user:
        if worker_name:
            await Transition.objects.create(worker_name=worker_name)
        new_user = await User.objects.create(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            worker=s_worker,
        )
        return new_user

    if user.worker != s_user.worker:
        if s_worker.is_active:
            await s_user.update(is_processing=True)

    await s_user.update(
        last_activity=datetime.datetime.now(),
        username=user.username,
        worker=s_worker if s_worker.is_active else s_user.worker,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    return s_user


@router.post("/date/")
async def get_or_create_user_date(
    user: schemas.UserCreate, last_activity: str, first_touch: str
) -> schemas.User:
    s_worker = await Worker.objects.get_or_none(id=user.worker)
    s_user = await User.objects.get_or_none(id=user.id)

    if not s_worker:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данный работник не был найден",
        )

    if s_user is not None:
        return await s_user.update(
            username=user.username,
            worker=s_worker,
            first_name=user.first_name,
            last_name=user.last_name,
            first_touch=first_touch,
            last_activity=last_activity,
            is_processing=True,
            is_free_consulting=True,
        )

    new_user = await User.objects.create(
        id=user.id,
        username=user.username,
        worker=s_worker,
        first_name=user.first_name,
        last_name=user.last_name,
        first_touch=first_touch,
        last_activity=last_activity,
        is_processing=True,
        is_free_consulting=True,
    )
    return new_user


@router.post("/free/")
async def update_user_free(user: schemas.UserCreate) -> schemas.User:
    s_user = await User.objects.get_or_none(id=user.id)
    return await s_user.update(is_free_consulting=True)


@router.get("/{user}/payment/details/")
async def get_user_payment_details(user: int) -> schemas.UserPaymentDetail:
    s_user = await User.objects.get_or_none(id=user)
    return await UserPaymentDetail.objects.filter(user=s_user).all()

@router.get("/payment/details/")
async def get_user_payment_detail(id: int) -> schemas.UserPaymentDetail:
    return await UserPaymentDetail.objects.get_or_none(id=id)


@router.post("/payment/details/")
async def create_payment_details(detail: schemas.UserPaymentDetailCreate) -> schemas.UserPaymentDetail:
    return await UserPaymentDetail.objects.create(
        name=detail.name,
        user=await User.objects.get_or_none(id=detail.user),
        text=detail.text
    )

@router.delete("/payment/details/{detail}")
async def delete_payment_detail(detail: int) -> None    :
    await UserPaymentDetail.objects.filter(id=detail).delete()


