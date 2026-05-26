import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATA_FILE = Path(os.getenv("DATA_FILE", BASE_DIR / "data.json"))
DEBUG = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"}
