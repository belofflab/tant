from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from src.database.connection import database
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.data.config import ALLOWED_ORIGINS
from src.routers import (
    info,
    users,
    workers,
    analytics,
    proxies,
    transitions,
    admin,
    messages,
    worker_requests,
    admin_requests,
    matrix_requests
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


@app.get("/api/v1/analytics/info/")
async def analytics_info(request: Request):
    return templates.TemplateResponse(
        "analytics.html",
        {"request": request},
    )


app.include_router(info.router)
app.include_router(proxies.router)
app.include_router(analytics.router)
app.include_router(users.router)
app.include_router(worker_requests.router)
app.include_router(matrix_requests.router)
app.include_router(messages.router)
app.include_router(workers.router)
app.include_router(admin.router)
app.include_router(transitions.router)
app.include_router(admin_requests.router)
