import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent
ENV_FILE = BASE_DIR / '.env'


if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

BANNER = BASE_DIR / "media/banner.jpeg"

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
ADMIN_IDS = os.getenv("ADMIN_IDS").split(" ")
SERVER_URL = os.getenv('SERVER_URL')
PROXY6_KEY=os.getenv("PROXY6_KEY")
CHANNEL_ID= int(os.getenv('CHANNEL_ID'))