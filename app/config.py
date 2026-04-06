import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [8369302291]
ADMIN_ID = ADMIN_IDS[0]
CHANNEL_ID_RAW = os.getenv("CHANNEL_ID", "").strip()
CHANNEL_ID = int(CHANNEL_ID_RAW) if CHANNEL_ID_RAW else None

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")
