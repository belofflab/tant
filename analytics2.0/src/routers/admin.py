import typing as t
from fastapi import APIRouter, HTTPException, status

from src import schemas
from src.database.models import (
    AdminRequest,
    AdminPaymentDetail,
    BotRequest,
    TransactionType,
    Bot,
)

router = APIRouter(prefix="/api/v1/admin", tags=["Административная панель"])


@router.get("/info/")
async def get_info() -> dict:
    wrequests = await BotRequest.objects.filter(is_success=True).all()
    arequests = await AdminRequest.objects.all()

    admin_total = sum(
        [
            arequest.amount
            if arequest.type == TransactionType.DEPOSIT
            else -(arequest.amount)
            for arequest in arequests
        ]
    )

    total = (
        sum(
            [
                request.amount
                if request.type == TransactionType.DEPOSIT
                else -(request.amount)
                for request in wrequests
            ]
        )
        + admin_total
    )
    marginal = (
        sum(
            [
                request.marginal_amount
                if request.type == TransactionType.DEPOSIT
                else -(request.marginal_amount)
                for request in wrequests
            ]
        )
        + admin_total
    )
    worker_total = sum(
        [
            request.worker_amount
            if request.type == TransactionType.DEPOSIT
            else -(request.worker_amount)
            for request in wrequests
        ]
    )

    data = {"total": total, "marginal": marginal, "owed": worker_total}

    return data


@router.post("/reward/")
async def reward(worker_request: schemas.WorkerRequestCreate):
    s_bot = await Bot.objects.get_or_none(uid=worker_request.bot_uid)
    await BotRequest.objects.create(
        bot=s_bot,
        amount=0,
        marginal_amount=-worker_request.amount,
        worker_amount=worker_request.amount,
        is_success=True,
        type=TransactionType.DEPOSIT,
    )
    await s_bot.update(amount=s_bot.amount + worker_request.amount)

@router.post("/penalty/")
async def penalty(worker_request: schemas.WorkerRequestCreate):
    s_bot = await Bot.objects.get_or_none(uid=worker_request.bot_uid)
    await BotRequest.objects.create(
        bot=s_bot,
        amount=0,
        marginal_amount=-worker_request.amount,
        worker_amount=worker_request.amount,
        is_success=True,
        type=TransactionType.WITHDRAWAL,
    )
    await s_bot.update(amount=s_bot.amount - worker_request.amount)


@router.post("/requests/")
async def create(admin_request: schemas.AdminRequestCreate) -> schemas.AdminRequest:
    wrequests = await BotRequest.objects.filter(type=TransactionType.DEPOSIT, is_success=True).all()
    arequests = await AdminRequest.objects.all()
    worker_total = sum([request.amount for request in wrequests])
    admin_total = sum(
        [
            arequest.amount
            if arequest.type == TransactionType.DEPOSIT
            else -(arequest.amount)
            for arequest in arequests
        ]
    )
    if admin_request.type == TransactionType.WITHDRAWAL:
        if not (admin_total + worker_total) - admin_request.amount >= 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Сумма вывода превышает доход!",
            )

    return await AdminRequest.objects.create(
        amount=admin_request.amount, type=admin_request.type
    )

@router.get("/payment/details/")
async def get_payment_details() -> t.List[schemas.AdminPaymentDetail]:
    return await AdminPaymentDetail.objects.all()


@router.get("/payment/details/{detail}")
async def get_payment_detail(detail: int) -> schemas.AdminPaymentDetail:
    return await AdminPaymentDetail.objects.get_or_none(id=detail)


@router.delete("/payment/details/{detail}")
async def delete_payment_detail(detail: int) -> None:
    await AdminPaymentDetail.objects.filter(id=detail).delete()


@router.post("/payment/details/")
async def create_payment_details(
    detail: schemas.AdminPaymentDetailCreate,
) -> schemas.AdminPaymentDetail:
    return await AdminPaymentDetail.objects.create(name=detail.name, text=detail.text)
