import typing as t

from fastapi import APIRouter, HTTPException, status, Request
from src.database.models import Message, User, Worker
from ormar import and_, or_
from fastapi.templating import Jinja2Templates
from src import schemas

router = APIRouter(prefix="/api/v1/messages", tags=["Сообщения"])
templates = Jinja2Templates(directory="templates")


@router.post("/")
async def create(message: schemas.MessageCreate) -> schemas.Message:
    sender = await User.objects.get_or_none(id=message.sender)
    receiver = await User.objects.get_or_none(id=message.receiver)
    worker = await Worker.objects.get_or_none(user__id=message.sender)

    if receiver is None:
        receiver = await User.objects.create(id=message.receiver, worker=worker)
    if sender is None:
        sender = await User.objects.create(id=message.sender, worker=worker)

    return await Message.objects.create(
        sender=sender,
        receiver=receiver,
        text=message.text,
        photo=message.photo,
        voice=message.voice,
    )


@router.get("/")
async def get(message: schemas.MessageGet) -> t.List[schemas.Message]:
    sender = await User.objects.get_or_none(id=message.sender)
    receiver = await User.objects.get_or_none(id=message.receiver)

    if sender is None or receiver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Один из участников чата не найден",
        )

    messages = (
        await Message.objects.filter(
            or_(
                and_(sender=sender, receiver=receiver),
                and_(sender=receiver, receiver=sender),
            )
        )
        .order_by("-date")
        .all()
    )

    print(messages)
    print(len(messages))

    return messages


@router.get("/{sender}/{receiver}/")
async def analytics_info(sender: int, receiver: int, request: Request):
    s_sender = await User.objects.get_or_none(id=sender)
    s_receiver = await User.objects.get_or_none(id=receiver)

    if s_sender is None or s_receiver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Один из участников чата не найден",
        )

    messages = (
        await Message.objects.filter(
            or_(
                and_(sender=sender, receiver=receiver),
                and_(sender=receiver, receiver=sender),
            )
        )
        .order_by("date")
        .all()
    )

    return templates.TemplateResponse(
        "messages.html",
        {
            "request": request,
            "sender": s_sender,
            "receiver": s_receiver,
            "messages": messages,
        },
    )
