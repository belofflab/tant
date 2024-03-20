import statistics
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status, Query
from src.database.models import User, Worker, Transition, WorkerRequest, TransactionType

router = APIRouter(prefix="/api/v1/analytics", tags=["Аналитика"])


@router.get("/chats/total/")
async def total_chats(
    worker: int = None,
    date_range: str = Query(
        None, description="Диапозон даты в формате 'dd.mm.yyyy dd.mm.yyyy'"
    ),
    disactive: bool = Query(False, description="Вытащить только неактивные чаты"),
):
    filter_params = {}
    if worker is not None:
        s_worker = await Worker.objects.get_or_none(user__id=worker)
        if s_worker:
            filter_params["worker"] = s_worker
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Работник не был найден"
            )

    if date_range and not disactive:
        start_date_str, end_date_str = date_range.split()

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)

        filter_params["first_touch__gte"] = start_date
        filter_params["first_touch__lte"] = end_date

    if disactive:
        now = datetime.now()
        filter_params["last_activity__lte"] = now - timedelta(days=7)

    return await User.objects.filter(**filter_params).prefetch_related("worker").all()


@router.get("/workers/conversion")
async def workers_conversion(
    link: str = Query(
        description="Введите ссылку на воркера https://t.me/bot_username?start=worker_username"
    ),
    date_range: str = Query(
        None, description="Диапозон даты в формате 'yyyy.mm.dd yyyy.mm.dd'"
    ),
):
    worker_name = link.split("?start=")[-1]
    filter_params = {}
    transition_params = {}
    if date_range:
        start_date_str, end_date_str = date_range.split()

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)

        filter_params["first_touch__gte"] = start_date
        filter_params["first_touch__lte"] = end_date
        transition_params["date__gte"] = start_date
        transition_params["date__lte"] = end_date

    all_transitions = await Transition.objects.filter(
        worker_name=worker_name, **transition_params
    ).all()
    button_transitions = (
        await User.objects.prefetch_related("worker")
        .filter(
            is_free_consulting=True,
            worker__username__icontains=worker_name,
            **filter_params
        )
        .all()
    )
    private_transitions = (
        await User.objects.prefetch_related("worker")
        .filter(
            is_processing=True, worker__username__icontains=worker_name, **filter_params
        )
        .all()
    )

    return {
        "all_transitions": len(all_transitions),
        "button_transitions": len(button_transitions),
        "private_transitions": len(private_transitions),
    }


@router.get("/total/conversion")
async def total_conversion(
    date_range: str = Query(
        None, description="Диапозон даты в формате 'yyyy.mm.dd yyyy.mm.dd'"
    ),
):
    filter_params = {}
    rates_params = {}
    if date_range:
        start_date_str, end_date_str = date_range.split()

        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        end_date = datetime.strptime(end_date_str, "%d.%m.%Y") + timedelta(days=1)

        filter_params["type"] = TransactionType.DEPOSIT
        filter_params["is_success"] = True
        filter_params["date__gte"] = start_date
        filter_params["date__lte"] = end_date

        rates_params["workerrequests__date__gte"] = start_date
        rates_params["workerrequests__date__lte"] = end_date
    total_worker_requests = [
        worker_request.amount
        for worker_request in await WorkerRequest.objects.filter(**filter_params).all()
    ]
    marginal_worker_requests = [
        worker_request.marginal_amount
        for worker_request in await WorkerRequest.objects.filter(**filter_params).all()
    ]

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
    filtered_workers = {}
    for worker in workers:
        tmp_worker_requests = [
                    worker_request.amount
                    for worker_request in worker.workerrequests
                ]
        filtered_workers[worker.name] = {
            "sum1": sum(tmp_worker_requests),
            "sum2": round(float(sum(tmp_worker_requests)) * (worker.comission / 100), 2),
            "sum3": round(float(sum(tmp_worker_requests)) - float(sum(tmp_worker_requests)) * (worker.comission / 100), 2),
            "avg": round(float(statistics.mean(tmp_worker_requests)), 2),
            "len": len(tmp_worker_requests)
        }

    return {
        "total": sum(total_worker_requests),
        "marginal": sum(marginal_worker_requests),
        "total_requests": len(total_worker_requests),
        "workers": filtered_workers,
    }
