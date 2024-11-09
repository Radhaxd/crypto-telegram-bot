
import asyncio
from pyrogram import Client, idle
from config.config import config
from database.db import init_db
from handlers.converter import convert_crypto, refresh_conversion
from handlers.start import start_command, handle_start_options
from handlers.quiz import start_quiz, handle_quiz_answer, show_leaderboard
from handlers.news import get_news, periodic_news_update
from handlers.admin import broadcast_message, handle_broadcast_response, moderate_user, toggle_feature
from handlers.user_management import handle_private_message, user_settings, set_user_setting, user_stats

app = Client("crypto_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

async def main():
    print("Initializing database...")
    await init_db()

    print("Registering handlers...")
    app.add_handler(convert_crypto)
    app.add_handler(refresh_conversion)
    app.add_handler(start_command)
    app.add_handler(handle_start_options)
    app.add_handler(start_quiz)
    app.add_handler(handle_quiz_answer)
    app.add_handler(show_leaderboard)
    app.add_handler(get_news)
    app.add_handler(broadcast_message)
    app.add_handler(handle_broadcast_response)
    app.add_handler(moderate_user)
    app.add_handler(toggle_feature)
    app.add_handler(handle_private_message)
    app.add_handler(user_settings)
    app.add_handler(set_user_setting)
    app.add_handler(user_stats)

    print("Starting bot...")
    await app.start()
    
    print("Starting periodic tasks...")
    asyncio.create_task(periodic_news_update())

    print("Bot is running. Press Ctrl+C to stop.")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
