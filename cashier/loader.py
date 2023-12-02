from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from utils.proxy.proxy6 import Proxy6

from data.config import BOT_TOKEN, PROXY6_KEY

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
proxy6 = Proxy6(api_key=PROXY6_KEY)
dp = Dispatcher(bot, storage=storage) 

