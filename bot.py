
import asyncio
from pyrogram import Client, idle
from config.config import config
from database.db import init_db
from handlers.converter import convert_crypto, refresh_conversion
from handlers.start import start_command, handle_start_options
from handlers.quiz import start_quiz, handle_quiz_answer, show_leaderboard, toggle_auto_quiz, auto_quiz_task, send_quiz, daily_question_rotation
from handlers.news import get_news, periodic_news_update
from handlers.admin import broadcast_message, show_stats, ban_unban_user
from handlers.user_management import handle_private_message, welcome_new_members, set_quiz_interval
from handlers.crypto_features import crypto_info, top_cryptocurrencies
from handlers.inline_query import inline_query
from handlers.user_preferences import user_settings, set_language, set_favorite_crypto
from handlers.price_alerts import set_price_alert, remove_price_alert, list_user_alerts, check_price_alerts
from handlers.trading_sim import check_balance, buy_crypto, sell_crypto, view_portfolio
from utils.logger import main_logger
from utils.i18n import i18n
from utils.rate_limit import rate_limit

app = Client("crypto_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

async def main():
    try:
        main_logger.info("Initializing database...")
        await init_db()

        main_logger.info("Registering handlers...")
        app.add_handler(convert_crypto)
        app.add_handler(refresh_conversion)
        app.add_handler(start_command)
        app.add_handler(handle_start_options)
        app.add_handler(start_quiz)
        app.add_handler(handle_quiz_answer)
        app.add_handler(show_leaderboard)
        app.add_handler(toggle_auto_quiz)
        app.add_handler(get_news)
        app.add_handler(broadcast_message)
        app.add_handler(show_stats)
        app.add_handler(ban_unban_user)
        app.add_handler(handle_private_message)
        app.add_handler(welcome_new_members)
        app.add_handler(set_quiz_interval)
        app.add_handler(crypto_info)
        app.add_handler(top_cryptocurrencies)
        app.add_handler(inline_query)
        app.add_handler(user_settings)
        app.add_handler(set_language)
        app.add_handler(set_favorite_crypto)
        app.add_handler(set_price_alert)
        app.add_handler(remove_price_alert)
        app.add_handler(list_user_alerts)
        app.add_handler(check_balance)
        app.add_handler(buy_crypto)
        app.add_handler(sell_crypto)
        app.add_handler(view_portfolio)

        main_logger.info("Starting bot...")
        await app.start()
        
        main_logger.info("Starting periodic tasks...")
        asyncio.create_task(periodic_news_update())
        asyncio.create_task(auto_quiz_task())
        asyncio.create_task(daily_question_rotation())
        asyncio.create_task(check_price_alerts())

        main_logger.info("Bot is running. Press Ctrl+C to stop.")
        await idle()
    except Exception as e:
        main_logger.error(f"An error occurred in main: {str(e)}", exc_info=True)
    finally:
        main_logger.info("Stopping bot...")
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
