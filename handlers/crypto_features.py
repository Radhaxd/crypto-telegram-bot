
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.cache import cached
from utils.logger import main_logger
import aiohttp

@cached(expiration=300)
async def get_crypto_info(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@Client.on_message(filters.command("info"))
async def crypto_info(client, message):
    try:
        _, crypto_id = message.text.split()
        info = await get_crypto_info(crypto_id.lower())
        
        response = f"💰 {info['name']} ({info['symbol'].upper()})\n\n"
        response += f"Current Price: ${info['market_data']['current_price']['usd']}\n"
        response += f"Market Cap: ${info['market_data']['market_cap']['usd']:,}\n"
        response += f"24h Change: {info['market_data']['price_change_percentage_24h']:.2f}%\n"
        response += f"All Time High: ${info['market_data']['ath']['usd']}\n"
        response += f"All Time Low: ${info['market_data']['atl']['usd']}\n"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Website", url=info['links']['homepage'][0])],
            [InlineKeyboardButton("📊 Chart", url=f"https://www.coingecko.com/en/coins/{crypto_id}")]
        ])
        
        await message.reply_text(response, reply_markup=keyboard)
    except Exception as e:
        main_logger.error(f"Error in crypto_info: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred or the cryptocurrency was not found.")

@Client.on_message(filters.command("top"))
async def top_cryptocurrencies(client, message):
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        
        response = "🏆 Top 10 Cryptocurrencies by Market Cap:\n\n"
        for i, coin in enumerate(data, 1):
            response += f"{i}. {coin['name']} (${coin['current_price']:.2f})\n"
        
        await message.reply_text(response)
    except Exception as e:
        main_logger.error(f"Error in top_cryptocurrencies: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while fetching top cryptocurrencies.")

# Add these handlers to your main bot file
