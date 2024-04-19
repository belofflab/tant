import typing as t
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from uuid import UUID
from src import schemas
from src.database.models import BotRequest, Bot, TransactionType
from src.utils import files

router = APIRouter(prefix="/api/v1/bots/requests", tags=["Заявки работников"])


async def find_bot(uid: str):
    worker_bot = await Bot.objects.filter(uid=uid).get_or_none()
    if not worker_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найден")
    return worker_bot


@router.post("/")
async def create(
    worker_request: schemas.WorkerRequestCreate = Depends(),
    receipt: t.Optional[UploadFile] = File(default=None),
) -> schemas.WorkerRequest:
    bot = await find_bot(worker_request.bot_uid)
    receipt_path = None
    if receipt:
        receipt_path = files.create(file=receipt, upath="receipts")

    if worker_request.type == TransactionType.WITHDRAWAL:
        if not worker_request.is_admin:
            if worker_request.amount > bot.amount - bot.freezed_amount:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Недостаточно для вывода",
                )
            await bot.update(freezed_amount=bot.freezed_amount + worker_request.amount)
        else:
            await bot.update(amount=bot.amount - worker_request.amount)
    elif worker_request.type == TransactionType.DEPOSIT:
        if worker_request.is_admin:
            await bot.update(
                amount=bot.amount + worker_request.amount,
            )

    if worker_request.is_admin:
        return await BotRequest.objects.create(
            worker=bot,
            amount=0,
            marginal_amount=0,
            worker_amount=worker_request.amount,
            is_success=True,
            receipt=receipt_path,
            type=worker_request.type,
        )

    marginal_amount = round(float(worker_request.amount) * (bot.comission / 100), 2)

    return await BotRequest.objects.create(
        bot=bot,
        amount=worker_request.amount,
        marginal_amount=(
            marginal_amount if worker_request.type == TransactionType.DEPOSIT else 0
        ),
        worker_amount=(
            worker_request.amount
            if worker_request.type == TransactionType.WITHDRAWAL
            else float(worker_request.amount) - marginal_amount
        ),
        receipt=receipt_path,
        type=worker_request.type,
    )


@router.get("/{request}")
async def get_request(request: int):
    bot_request = await BotRequest.objects.prefetch_related("bot").get_or_none(
        id=request
    )
    if bot_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена"
        )

    return bot_request


@router.get("/")
async def get_all() -> t.List[schemas.WorkerRequest]:
    return await BotRequest.objects.order_by("-date").all()


@router.get("/{bot_uid}/")
async def get_by_bot(bot_uid: UUID) -> t.List[schemas.WorkerRequest]:
    bot = await find_bot(bot_uid)
    return await BotRequest.objects.filter(bot=bot).order_by("-date").all()


@router.patch("/")
async def update_status(
    worker_request: schemas.WorkerRequestPatch,
) -> schemas.WorkerRequest:
    s_bot_request = await BotRequest.objects.get_or_none(id=worker_request.id)
    s_bot = await Bot.objects.get(id=s_bot_request.bot)
    if not worker_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена"
        )
    if s_bot_request.type == TransactionType.WITHDRAWAL:
        if worker_request.is_success:
            await s_bot.update(
                amount=s_bot.amount - s_bot_request.amount,
                freezed_amount=s_bot.freezed_amount - s_bot_request.amount,
            )
        else:
            await s_bot.update(
                freezed_amount=s_bot.freezed_amount - s_bot_request.amount,
            )

    elif s_bot_request.type == TransactionType.DEPOSIT:
        if worker_request.is_success:
            await s_bot.update(
                amount=s_bot.amount + s_bot_request.worker_amount,
            )

    return await s_bot_request.update(
        is_success=worker_request.is_success, comment=worker_request.comment
    )
