from fastapi import APIRouter, Response

from src import schemas
from src.database import models
from src.utils.auth.handler import sign_jwt
from src.utils.hashing import Hasher

router = APIRouter(prefix='/api/v1/auth', tags=['Авторизация'])



@router.post('/signin')
async def signin(user: schemas.UserCreate):
    q_user = await models.Profile.objects.get_or_none(email=user.email)
    if not q_user or not Hasher.verify_password(user.password, q_user.password):
        return Response(status_code=403, content='Неверная почта или пароль')
    access_token = sign_jwt(user_id=q_user.idx, email=q_user.email)
    await q_user.update(access_token=access_token)
    q_user.password = ''
    return q_user
    


@router.post('/signup')
async def signup(user: schemas.UserCreate) -> schemas.User:
    q_user = await models.Profile.objects.get_or_none(email=user.email)
    if q_user is not None:
        return Response(status_code=403, content='Пользователь уже существует')
    user.password = Hasher.get_password_hash(user.password)
    new_user =  await models.User.objects.create(**user.dict())
    access_token = sign_jwt(user_id=new_user.idx, email=new_user.email)
    await q_user.update(access_token=access_token)
    new_user.password = ''

    return new_user