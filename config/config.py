
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGO_URI = os.getenv("MONGO_URI")
    CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

config = Config()
