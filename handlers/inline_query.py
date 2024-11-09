
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from utils.cache import cached
from utils.logger import main_logger
import aiohttp

@cached(expiration=300)
async def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data.get(crypto_id, {}).get('usd')

@Client.on_inline_query()
async def inline_query(client, inline_query):
    try:
        query = inline_query.query.lower()
        results = []

        if query:
            price = await get_crypto_price(query)
            if price:
                results.append(
                    InlineQueryResultArticle(
                        title=f"{query.upper()} Price",
                        description=f"${price}",
                        input_message_content=InputTextMessageContent(
                            f"💰 The current price of {query.upper()} is ${price}"
                        )
                    )
                )

        await inline_query.answer(results=results, cache_time=300)
    except Exception as e:
        main_logger.error(f"Error in inline_query: {str(e)}", exc_info=True)
