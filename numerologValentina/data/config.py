import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

BANNER = BASE_DIR / "media/banner.jpg"
VALENTINA = BASE_DIR / "media/valentina.jpg"
ASKEZA = BASE_DIR / "media/askeza.jpg"

if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TRAINING_CHANNEL = int(os.getenv("TRAINING_CHANNEL"))
ADMIN_IDS = os.getenv("ADMIN_IDS").split()
SERVER_URL = os.getenv("SERVER_URL")
QIWI_BILL_LIFETIME = int(os.getenv("QIWI_BILL_LIFETIME"))
QIWI_PAYMENT_ATTEMPT = int(os.getenv("QIWI_PAYMENT_ATTEMPT"))
QIWI_PRIVATE_KEY = os.getenv("QIWI_PRIVATE_KEY")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
