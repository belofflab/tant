import os
from dotenv import load_dotenv
from pathlib import Path
BASE_DIR = Path(__name__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

WDATA_PATH = "data/worker.json"

BANNER = BASE_DIR / "media/banner.jpg"
WORKER_PHOTO = BASE_DIR / "media/worker.jpg"
ASKEZA = BASE_DIR  / "media/askeza.jpg"
VIKTORIA = BASE_DIR / "media/viktoria.jpg"

if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

ANALYTICS_TOKEN = os.getenv("ANALYTICS_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")

WEB_APP_DOMAIN = os.getenv("WEB_APP_DOMAIN", "...TODO")
WEB_APP_HOST = os.getenv("WEB_APP_HOST", "0.0.0.0")
WEB_APP_PORT = int(os.getenv("WEB_APP_PORT", 8000))
WEB_APP_WEBHOOK = os.getenv("WEB_APP_WEBHOOK", "/hook")

SERVER_URL = os.getenv("SERVER_URL")