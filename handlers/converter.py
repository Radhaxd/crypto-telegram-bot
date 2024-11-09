
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import config
import aiohttp
from utils.cache import cached
from utils.logger import main_logger
from utils.i18n import i18n
from database.db import get_user

@cached(expiration=300)
async def get_conversion_rate(from_currency, to_currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_currency}&vs_currencies={to_currency}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data[from_currency][to_currency]

@Client.on_message(filters.command("convert"))
async def convert_crypto(client, message):
    try:
        user = await get_user(message.from_user.id)
        lang = user.get('language', 'en') if user else 'en'

        _, amount, from_currency, to_currency = message.text.split()
        amount = float(amount)
        
        rate = await get_conversion_rate(from_currency.lower(), to_currency.lower())
        converted_amount = amount * rate

        response = i18n.get_text("convert_result", lang, amount=amount, from_currency=from_currency.upper(), 
                                 converted_amount=converted_amount, to_currency=to_currency.upper())
        response += "\n" + i18n.get_text("current_price", lang, currency=to_currency.upper(), price=rate)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{amount}_{from_currency}_{to_currency}")]
        ])

        await message.reply_text(response, reply_markup=keyboard)
    except Exception as e:
        main_logger.error(f"Error in convert_crypto: {str(e)}", exc_info=True)
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_callback_query(filters.regex("^refresh_"))
async def refresh_conversion(client, callback_query):
    try:
        user = await get_user(callback_query.from_user.id)
        lang = user.get('language', 'en') if user else 'en'

        _, amount, from_currency, to_currency = callback_query.data.split("_")
        amount = float(amount)
        
        rate = await get_conversion_rate(from_currency.lower(), to_currency.lower())
        converted_amount = amount * rate

        response = i18n.get_text("convert_result", lang, amount=amount, from_currency=from_currency.upper(), 
                                 converted_amount=converted_amount, to_currency=to_currency.upper())
        response += "\n" + i18n.get_text("current_price", lang, currency=to_currency.upper(), price=rate)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{amount}_{from_currency}_{to_currency}")]
        ])

        await callback_query.edit_message_text(response, reply_markup=keyboard)
    except Exception as e:
        main_logger.error(f"Error in refresh_conversion: {str(e)}", exc_info=True)
        await callback_query.answer("An error occurred while refreshing the conversion.")
