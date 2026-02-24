import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8369302291

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")