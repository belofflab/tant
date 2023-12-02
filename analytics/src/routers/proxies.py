import typing as t

from fastapi import APIRouter, HTTPException, status, Depends
from src.database.models import Proxy
from src import schemas

router = APIRouter(prefix="/api/v1/proxies", tags=["Прокси"])


@router.get("/")
async def get_available_proxies() -> t.List[schemas.Proxy]:
    return await Proxy.objects.all()

@router.post("/")
async def create_proxy(proxy: schemas.ProxyCreate = Depends()) -> schemas.Proxy:
    return await Proxy.objects.create(**proxy.dict())