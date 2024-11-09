
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    welcome_message = (
        "👋 Welcome to the Crypto Bot! 🤖\n\n"
        "I'm here to help you with all things crypto. Here's what I can do:\n"
        "• Convert between cryptocurrencies\n"
        "• Provide the latest crypto news\n"
        "• Test your crypto knowledge with quizzes\n"
        "• And much more!\n\n"
        "Choose an option below to get started:"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📈 Price Check", callback_data="price_check")],
        [InlineKeyboardButton("🧩 Crypto Quiz", callback_data="crypto_quiz")],
        [InlineKeyboardButton("📰 Latest News", callback_data="latest_news")],
        [InlineKeyboardButton("🔄 Converter", callback_data="converter")]
    ])

    await message.reply_text(welcome_message, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("^(price_check|crypto_quiz|latest_news|converter)$"))
async def handle_start_options(client, callback_query):
    option = callback_query.data

    if option == "price_check":
        await callback_query.answer("Use /convert command to check prices and convert cryptocurrencies.")
    elif option == "crypto_quiz":
        await callback_query.answer("Use /quiz command to start a crypto quiz.")
    elif option == "latest_news":
        await callback_query.answer("Use /news command to get the latest crypto news.")
    elif option == "converter":
        await callback_query.answer("Use /convert command to convert between cryptocurrencies.")
