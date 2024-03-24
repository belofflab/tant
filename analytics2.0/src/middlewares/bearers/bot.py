from typing import Any, Coroutine
from fastapi import status, HTTPException

from .jwt import JWTBearer
from src.database.models import Bot


class BotBearer(JWTBearer):
  def __init__(self, auto_error: bool = True):
    super().__init__(auto_error)