from fastapi import APIRouter, Depends
from src.middlewares.auth import JWTBearer

router = APIRouter(prefix='/api/v1/info', tags=['Информация'])



@router.get('/', dependencies=[Depends(JWTBearer())])
async def info(): return {"created_by": "Beloff Laboratory https://belofflab.com/"}