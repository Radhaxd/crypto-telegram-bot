
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config.config import config
from database.db import save_news, get_latest_news
import aiohttp
import asyncio

async def fetch_crypto_news():
    url = f"https://newsapi.org/v2/everything?q=cryptocurrency&apiKey={config.NEWS_API_KEY}&pageSize=5"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data.get('articles', [])

@Client.on_message(filters.command("news"))
async def get_news(client, message):
    news_articles = await get_latest_news()
    
    if not news_articles:
        news_articles = await fetch_crypto_news()
        await save_news(news_articles)
    
    for article in news_articles:
        news_text = (
            f"📰 {article['title']}\n\n"
            f"{article['description']}\n\n"
            f"Source: {article['source']['name']}"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Read More", url=article['url'])]
        ])
        
        await message.reply_text(news_text, reply_markup=keyboard)

async def periodic_news_update():
    while True:
        news_articles = await fetch_crypto_news()
        await save_news(news_articles)
        await asyncio.sleep(3600)  # Update every hour

# Add this to your main bot file to start the periodic update
# asyncio.create_task(periodic_news_update())
