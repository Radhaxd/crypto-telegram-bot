
from pyrogram import Client, filters
from database.db import get_user, create_user, update_user

@Client.on_message(filters.private)
async def handle_private_message(client, message):
    user = await get_user(message.from_user.id)
    if not user:
        user_data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "joined_date": message.date
        }
        await create_user(user_data)

@Client.on_message(filters.command("settings"))
async def user_settings(client, message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.reply_text("You don't have any settings yet.")
        return

    settings_text = "Your current settings:\n"
    for key, value in user.items():
        if key.startswith("setting_"):
            settings_text += f"{key[8:]}: {value}\n"

    await message.reply_text(settings_text)

@Client.on_message(filters.command("set"))
async def set_user_setting(client, message):
    if len(message.text.split()) != 3:
        await message.reply_text("Usage: /set [setting_name] [value]")
        return

    _, setting_name, value = message.text.split()
    await update_user(message.from_user.id, {f"setting_{setting_name}": value})
    await message.reply_text(f"Setting '{setting_name}' has been updated to '{value}'.")

@Client.on_message(filters.command("stats"))
async def user_stats(client, message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.reply_text("No stats available.")
        return

    stats_text = "Your stats:\n"
    stats_text += f"Quiz Score: {user.get('quiz_score', 0)}\n"
    stats_text += f"Conversions Made: {user.get('conversions_made', 0)}\n"
    stats_text += f"News Articles Read: {user.get('news_read', 0)}\n"

    await message.reply_text(stats_text)
