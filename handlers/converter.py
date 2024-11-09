
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import config
import aiohttp

async def get_conversion_rate(from_currency, to_currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={from_currency}&vs_currencies={to_currency}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data[from_currency][to_currency]

@Client.on_message(filters.command("convert"))
async def convert_crypto(client, message):
    try:
        _, amount, from_currency, to_currency = message.text.split()
        amount = float(amount)
        
        rate = await get_conversion_rate(from_currency.lower(), to_currency.lower())
        converted_amount = amount * rate

        response = f"✨ {amount} {from_currency.upper()} = {converted_amount:.6f} {to_currency.upper()}\n"
        response += f"✨ Current {to_currency.upper()} Price: ${rate:.6f}"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{amount}_{from_currency}_{to_currency}")]
        ])

        await message.reply_text(response, reply_markup=keyboard)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_callback_query(filters.regex("^refresh_"))
async def refresh_conversion(client, callback_query):
    _, amount, from_currency, to_currency = callback_query.data.split("_")
    amount = float(amount)
    
    rate = await get_conversion_rate(from_currency.lower(), to_currency.lower())
    converted_amount = amount * rate

    response = f"✨ {amount} {from_currency.upper()} = {converted_amount:.6f} {to_currency.upper()}\n"
    response += f"✨ Current {to_currency.upper()} Price: ${rate:.6f}"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_{amount}_{from_currency}_{to_currency}")]
    ])

    await callback_query.edit_message_text(response, reply_markup=keyboard)
