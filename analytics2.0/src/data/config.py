import os 
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__name__).resolve().parent
ENV_FILE = BASE_DIR / '.env'

if os.path.exists(ENV_FILE):
  load_dotenv(ENV_FILE)


ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS').split()
DATABASE_URL = os.getenv('DATABASE_URL')