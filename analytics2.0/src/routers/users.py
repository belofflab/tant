import datetime
import typing as t

from fastapi import APIRouter, HTTPException, status
from src.database.models import Profile
from src import schemas

router = APIRouter(prefix="/api/v1/users", tags=["Пользователи"])


