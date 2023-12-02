import typing as t
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Query
from src.database.models import Worker, Proxy, TransactionType

from src import schemas

router = APIRouter(prefix="/api/v1/workers", tags=["Работники"])


@router.get("/{worker_id}")
async def get_worker(worker_id: int) -> schemas.Worker:
    s_worker = await Worker.objects.get_or_none(id=worker_id)
    if not s_worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вас нет в системе"
        )

    return s_worker


@router.get("/rates/")
async def get_workers_rates(
    date_range: str = Query(
        None, description="Диапозон даты в формате 'yyyy-mm-dd yyyy-mm-dd'"
    )
):
    rates_params = {}
    if date_range:
        start_date_str, end_date_str = date_range.split()

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        rates_params["workerrequests__date__gte"] = start_date
        rates_params["workerrequests__date__lte"] = end_date
    workers = (
        await Worker.objects.prefetch_related("workerrequests")
        .filter(
            **rates_params,
            workerrequests__is_success=True,
            workerrequests__amount__gt=0,
            workerrequests__type=TransactionType.DEPOSIT,
            is_active=True
        )
        .all()
    )
    result = {}
    for worker in workers:
        result[worker.name] = sum(
            [worker_request.worker_amount for worker_request in worker.workerrequests]
        )
    return result


@router.post("/")
async def update_or_create_worker(worker: schemas.WorkerCreate = Depends()):
    s_worker = await Worker.objects.get_or_none(id=worker.id)
    # s_user = await User.objects.get_or_none(id=worker.id)
    s_proxy = await Proxy.objects.get_or_none(id=worker.proxy)

    # if s_user is None:
    #     await User.objects.create(id=worker.id, username=worker.username)

    if s_proxy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мы не нашли прокси в системе",
        )
    if s_worker:
        if s_worker.proxy.id != worker.proxy:
            await s_worker.update(proxy=s_proxy)
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Мы успешно обновили прокси у работника",
            )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Работник уже подключен к системе",
        )

    new_worker = await Worker.objects.create(
        id=worker.id,
        name=worker.name,
        username=worker.username,
        freezed_amount=0,
        comission=50,
        api_hash=worker.api_hash,
        api_id=worker.api_id,
        proxy=worker.proxy,
    )

    return new_worker


@router.get("/")
async def get_workers() -> t.List[schemas.Worker]:
    return await Worker.objects.filter(is_active=True).prefetch_related("proxy").all()


@router.post("/fill/")
async def fill_worker_amount(worker: schemas.WorkerAmountUpdate):
    s_worker = await Worker.objects.get_or_none(id=worker.id)
    if s_worker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден"
        )

    return await s_worker.update(amount=s_worker.amount + worker.amount)


@router.post("/disable/{worker}")
async def disable_worker(worker: int):
    s_worker = await Worker.objects.get_or_none(id=worker)
    if s_worker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден"
        )

    return await s_worker.update(is_active=False)
