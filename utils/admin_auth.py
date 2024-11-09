
from functools import wraps
from pyrogram import Client, filters
from database.db import get_user

ADMIN_USER_IDS = [12345678]  # Replace with actual admin user IDs

def is_admin(func):
    @wraps(func)
    async def wrapper(client, message):
        user = await get_user(message.from_user.id)
        if message.from_user.id in ADMIN_USER_IDS or (user and user.get('is_admin', False)):
            return await func(client, message)
        else:
            await message.reply_text("You don't have permission to use this command.")
    return wrapper
