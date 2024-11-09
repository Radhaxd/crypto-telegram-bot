
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

# ... (keep existing database functions)

async def add_price_alert(user_id, crypto, price, condition):
    alert = {
        "user_id": user_id,
        "crypto": crypto,
        "price": price,
        "condition": condition,
        "created_at": datetime.now()
    }
    result = await db.price_alerts.insert_one(alert)
    return result.inserted_id

async def remove_price_alert(user_id, alert_id):
    result = await db.price_alerts.delete_one({"_id": alert_id, "user_id": user_id})
    return result.deleted_count > 0

async def get_user_alerts(user_id):
    cursor = db.price_alerts.find({"user_id": user_id})
    return await cursor.to_list(length=None)

async def get_all_active_alerts():
    cursor = db.price_alerts.find()
    return await cursor.to_list(length=None)

async def get_user_balance(user_id):
    user = await db.users.find_one({"user_id": user_id})
    return user.get("balance", 1000)  # Default starting balance of $1000

async def update_user_balance(user_id, new_balance):
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {"balance": new_balance}},
        upsert=True
    )

async def add_trade(user_id, trade_type, crypto, amount, price):
    trade = {
        "user_id": user_id,
        "type": trade_type,
        "crypto": crypto,
        "amount": amount,
        "price": price,
        "timestamp": datetime.now()
    }
    await db.trades.insert_one(trade)

async def get_user_trades(user_id):
    cursor = db.trades.find({"user_id": user_id})
    return await cursor.to_list(length=None)
