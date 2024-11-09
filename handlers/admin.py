
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_user, update_user, get_all_users, get_user_stats
from config.config import config
from utils.admin_auth import is_admin
from utils.logger import main_logger
from utils.i18n import i18n

@Client.on_message(filters.command("broadcast") & filters.user(config.ADMIN_USER_IDS))
@is_admin
async def broadcast_message(client, message):
    try:
        if len(message.text.split()) < 2:
            await message.reply_text("Please provide a message to broadcast.")
            return

        broadcast_message = message.text.split(None, 1)[1]
        
        users = await get_all_users()
        success_count = 0
        for user in users:
            try:
                await client.send_message(user['user_id'], broadcast_message)
                success_count += 1
            except Exception as e:
                main_logger.error(f"Failed to send broadcast to user {user['user_id']}: {str(e)}")
        
        await message.reply_text(f"Broadcast sent successfully to {success_count} out of {len(users)} users.")
    except Exception as e:
        main_logger.error(f"Error in broadcast_message: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while broadcasting the message.")

@Client.on_message(filters.command("stats") & filters.user(config.ADMIN_USER_IDS))
@is_admin
async def show_stats(client, message):
    try:
        stats = await get_user_stats()
        response = "📊 Bot Statistics:\n\n"
        response += f"Total Users: {stats['total_users']}\n"
        response += f"Active Users (last 24h): {stats['active_users']}\n"
        response += f"Total Quizzes Taken: {stats['total_quizzes']}\n"
        response += f"Total Conversions: {stats['total_conversions']}\n"
        
        await message.reply_text(response)
    except Exception as e:
        main_logger.error(f"Error in show_stats: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while fetching statistics.")

@Client.on_message(filters.command(["ban", "unban"]) & filters.user(config.ADMIN_USER_IDS))
@is_admin
async def ban_unban_user(client, message):
    try:
        command = message.text.split()[0][1:]
        if len(message.text.split()) != 2:
            await message.reply_text(f"Usage: /{command} <user_id>")
            return

        user_id = int(message.text.split()[1])
        user = await get_user(user_id)
        if not user:
            await message.reply_text("User not found.")
            return

        if command == "ban":
            await update_user(user_id, {"is_banned": True})
            await message.reply_text(f"User {user_id} has been banned.")
        else:
            await update_user(user_id, {"is_banned": False})
            await message.reply_text(f"User {user_id} has been unbanned.")
    except Exception as e:
        main_logger.error(f"Error in ban_unban_user: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while processing the command.")
