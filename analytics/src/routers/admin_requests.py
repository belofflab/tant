import typing as t
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File

from src import schemas
from src.database.models import WorkerRequest, Worker, TransactionType, AdminRequest
from src.utils import files

router = APIRouter(prefix="/api/v1/admin/requests", tags=["Заявки администратора"])


@router.post("/")
async def create(admin_request: schemas.AdminRequestCreate) -> schemas.AdminRequest:
    wrequests = await WorkerRequest.objects.filter(type=TransactionType.DEPOSIT, is_success=True).all()
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