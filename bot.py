
import asyncio
from pyrogram import Client, filters
from config import config
from database.db import init_db
from handlers import register_handlers

app = Client("crypto_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

async def main():
    await init_db()
    register_handlers(app)
    await app.start()
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
