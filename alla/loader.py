import json 

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from utils.api.analytics import Analytics

from data.config import BOT_TOKEN, BASE_DIR, WDATA_PATH

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage) 
analytics = Analytics()
analytics.start()


WDATA = json.loads(open(BASE_DIR / WDATA_PATH, "r", encoding="utf-8").read())
workers = WDATA.get("workers", [])
if len(workers) > 0:
  WORKER_USERNAME = WDATA["workers"][0]["user"]["username"]
else:
  WORKER_USERNAME = "username"