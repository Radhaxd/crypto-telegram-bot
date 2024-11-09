
from motor.motor_asyncio import AsyncIOMotorClient
from config.config import config

client = AsyncIOMotorClient(config.MONGO_URI)
db = client.crypto_bot

async def init_db():
    try:
        await client.admin.command('ping')
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

# User operations
async def get_user(user_id):
    return await db.users.find_one({"user_id": user_id})

async def create_user(user_data):
    await db.users.insert_one(user_data)

async def update_user(user_id, update_data):
    await db.users.update_one({"user_id": user_id}, {"$set": update_data})

# Quiz operations
async def save_quiz_score(user_id, score):
    await db.quiz_scores.update_one(
        {"user_id": user_id},
        {"$inc": {"score": score}},
        upsert=True
    )

async def get_leaderboard(limit=10):
    cursor = db.quiz_scores.find().sort("score", -1).limit(limit)
    return await cursor.to_list(length=limit)

# News operations
async def save_news(news_data):
    await db.news.insert_many(news_data)

async def get_latest_news(limit=5):
    cursor = db.news.find().sort("published_at", -1).limit(limit)
    return await cursor.to_list(length=limit)

async def get_auto_quiz_groups():
    cursor = db.users.find({"auto_quiz_enabled": True})
    return await cursor.to_list(length=None)
