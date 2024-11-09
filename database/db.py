
from motor.motor_asyncio import AsyncIOMotorClient
from config.config import config
from datetime import datetime, timedelta

client = AsyncIOMotorClient(config.MONGO_URI)
db = client.crypto_bot

async def init_db():
    try:
        await client.admin.command('ping')
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

async def get_user(user_id):
    return await db.users.find_one({"user_id": user_id})

async def create_user(user_data):
    await db.users.insert_one(user_data)

async def update_user(user_id, update_data):
    await db.users.update_one({"user_id": user_id}, {"$set": update_data})

async def get_all_users():
    cursor = db.users.find()
    return await cursor.to_list(length=None)

async def get_user_stats():
    total_users = await db.users.count_documents({})
    active_users = await db.users.count_documents({"last_activity": {"$gte": datetime.now() - timedelta(days=1)}})
    total_quizzes = await db.quiz_scores.count_documents({})
    total_conversions = await db.conversions.count_documents({})

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_quizzes": total_quizzes,
        "total_conversions": total_conversions
    }

async def save_quiz_score(user_id, score):
    await db.quiz_scores.update_one(
        {"user_id": user_id},
        {"$inc": {"score": score}},
        upsert=True
    )

async def get_leaderboard(limit=10):
    cursor = db.quiz_scores.find().sort("score", -1).limit(limit)
    return await cursor.to_list(length=limit)

async def save_conversion(user_id, from_currency, to_currency, amount):
    await db.conversions.insert_one({
        "user_id": user_id,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "timestamp": datetime.now()
    })

async def get_user_preferences(user_id):
    user = await get_user(user_id)
    return user.get('preferences', {})

async def update_user_preferences(user_id, preferences):
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"preferences": preferences}}
    )
