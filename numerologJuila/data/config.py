import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

BANNER = BASE_DIR / "media/banner.jpg"
WORKER_PHOTO = BASE_DIR / "media/worker.jpg"
ASKEZA = BASE_DIR  / "media/askeza.jpg"
VIKTORIA = BASE_DIR / "media/viktoria.jpg"

if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

WORKER_USERNAME = os.getenv("WORKER_USERNAME")
TRAINING_CHANNEL = -100 # TODO
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", -100))
ADMIN_IDS = os.getenv("ADMIN_IDS").split()
SERVER_URL = os.getenv("SERVER_URL")
