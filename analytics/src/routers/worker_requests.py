import typing as t
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File

from src import schemas
from src.database.models import WorkerRequest, Worker, TransactionType
from src.utils import files

router = APIRouter(prefix="/api/v1/worker/requests", tags=["Заявки работников"])


@router.post("/")
async def create(
    worker_request: schemas.WorkerRequestCreate = Depends(),
    receipt: t.Optional[UploadFile] = File(default=None),
) -> schemas.WorkerRequest:
    worker = await Worker.objects.get_or_none(user__id=worker_request.worker)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден"
        )
    receipt_path = None
    if receipt:
        receipt_path = files.create(file=receipt, upath="receipts")

    if worker_request.type == TransactionType.WITHDRAWAL:
        if not worker_request.is_admin:
            if worker_request.amount > worker.amount - worker.freezed_amount:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Недостаточно для вывода",
                )
            await worker.update(
                freezed_amount=worker.freezed_amount + worker_request.amount
            )
        else:
            await worker.update(amount=worker.amount - worker_request.amount)
    elif worker_request.type == TransactionType.DEPOSIT:
        if worker_request.is_admin:
            await worker.update(
                amount=worker.amount + worker_request.amount,
            )

    if worker_request.is_admin:
        return await WorkerRequest.objects.create(
            worker=worker,
            amount=0,
            marginal_amount=0,
            worker_amount=worker_request.amount,
            is_success=True,
            receipt=receipt_path,
            type=worker_request.type,
        )

    marginal_amount = round(float(worker_request.amount) * (worker.comission / 100), 2)

    return await WorkerRequest.objects.create(
        worker=worker,
        amount=worker_request.amount,
        marginal_amount=marginal_amount if worker_request.type == TransactionType.DEPOSIT else 0,
        worker_amount=worker_request.amount if worker_request.type == TransactionType.WITHDRAWAL else float(worker_request.amount) - marginal_amount,
        receipt=receipt_path,
        type=worker_request.type,
    )


@router.get("/{request}")
async def get_request(request: int):
    s_worker_request = await WorkerRequest.objects.prefetch_related(
        "worker"
    ).get_or_none(id=request)
    if not s_worker_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена"
        )

    return s_worker_request


@router.get("/")
async def get_all() -> t.List[schemas.WorkerRequest]:
    return await WorkerRequest.objects.order_by("-date").all()


@router.get("/{worker}/")
async def get_by_worker(worker: int) -> t.List[schemas.WorkerRequest]:
    s_worker = await Worker.objects.get_or_none(user__id=worker)
    if s_worker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден"
        )

    return await WorkerRequest.objects.filter(worker=s_worker).order_by("-date").all()


@router.patch("/")
async def update_status(
    worker_request: schemas.WorkerRequestPatch,
) -> schemas.WorkerRequest:
    s_worker_request = await WorkerRequest.objects.get_or_none(id=worker_request.id)
    s_worker = await Worker.objects.get(user__id=s_worker_request.worker)
    if not worker_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена"
        )
    if s_worker_request.type == TransactionType.WITHDRAWAL:
        if worker_request.is_success:
            await s_worker.update(
                amount=s_worker.amount - s_worker_request.amount,
                freezed_amount=s_worker.freezed_amount - s_worker_request.amount,
            )
        else:
            await s_worker.update(
                freezed_amount=s_worker.freezed_amount - s_worker_request.amount,
            )

    elif s_worker_request.type == TransactionType.DEPOSIT:
        if worker_request.is_success:
            await s_worker.update(
                amount=s_worker.amount + s_worker_request.worker_amount,
            )

    return await s_worker_request.update(
        is_success=worker_request.is_success, comment=worker_request.comment
    )
