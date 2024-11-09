
import aiohttp
from config.config import config

async def get_crypto_price(crypto_id, vs_currency='usd'):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={vs_currency}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data.get(crypto_id, {}).get(vs_currency)

async def format_large_number(number):
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f}B"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.2f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.2f}K"
    else:
        return f"{number:.2f}"

async def get_crypto_info(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
