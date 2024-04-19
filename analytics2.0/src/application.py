from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.database.connection import database
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.data.config import ALLOWED_ORIGINS
from src.routers import (
    info,
    tgusers,
    admin,
    bot_requests,
    bots
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


app.include_router(info.router)
app.include_router(tgusers.router)
app.include_router(bots.router)
app.include_router(bot_requests.router)
app.include_router(admin.router)