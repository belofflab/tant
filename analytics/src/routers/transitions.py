import typing as t
from fastapi import APIRouter, HTTPException, status
from src.database.models import Transition, User
from src import schemas

router = APIRouter(prefix="/api/v1/transitions", tags=["Переходы"])


@router.post("/")
async def create_transition(user_id: int , transition: schemas.TransitionCreate) -> schemas.Transition:
    is_user = await User.objects.get_or_none(id=user_id)
    print(is_user)
    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь уже в базе")
    return await Transition.objects.create(worker_name=transition.worker_name)

@router.get("/{worker_name}/")
async def get_transitions(worker_name: str) -> t.List[schemas.Transition]:
    return {"quantity": len(await Transition.objects.filter(worker_name=worker_name).all())}