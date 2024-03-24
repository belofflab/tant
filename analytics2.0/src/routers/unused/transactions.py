from datetime import datetime, timedelta
import typing as t

from fastapi import APIRouter, Query
# from src.database.models import Transaction
from src import schemas

router = APIRouter(prefix="/api/v1/transactions", tags=["Транзакции"])


@router.get("/")
async def workers_conversion(
    workers: str = Query(None, description="Введите воркеров в формате: id id id"),
    date_range: str = Query(
        None, description="Диапозон даты в формате 'yyyy.mm.dd yyyy.mm.dd'"
    ),
):
    transaction_params = {}
    if not workers:
        return {}
    cleaned_workers = workers.split()
    if date_range:
        start_date_str, end_date_str = date_range.split()

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1)

        transaction_params["date__gte"] = start_date
        transaction_params["date__lte"] = end_date

    total = 0

    for worker in cleaned_workers:
        s_worker = await Transaction.objects.filter(worker=int(worker), **transaction_params).get_or_none()
        if s_worker:
            total += s_worker.amount

    return {"total": total}
