
from pyrogram import Client, filters
from database.db import get_user, create_user, update_user

@Client.on_message(filters.new_chat_members)
async def welcome_new_members(client, message):
    new_members = message.new_chat_members
    for member in new_members:
        if member.is_self:  # Check if the new member is our bot
            welcome_text = (
                "👋 Hello! I'm CryptoQuizBot, your friendly cryptocurrency quiz master. 🤖\n\n"
                "Here's what I can do:\n"
                "• Send automatic quizzes (when enabled)\n"
                "• Provide crypto conversions\n"
                "• Share the latest crypto news\n\n"
                "To enable automatic quizzes, an admin can use the command /enable_quiz.\n"
                "To disable, use /disable_quiz.\n"
                "To set quiz interval, use /set_quiz_interval [minutes].\n\n"
                "Enjoy learning about crypto! 🚀"
            )
            await message.reply_text(welcome_text)

@Client.on_message(filters.command("set_quiz_interval") & filters.group)
async def set_quiz_interval(client, message):
    if len(message.text.split()) != 2:
        await message.reply_text("Usage: /set_quiz_interval [minutes]")
        return

    try:
        interval = int(message.text.split()[1])
        if interval < 1:
            raise ValueError("Interval must be at least 1 minute")
    except ValueError:
        await message.reply_text("Please provide a valid number of minutes (minimum 1).")
        return

    chat_id = message.chat.id
    chat_data = await get_user(chat_id) or {"chat_id": chat_id}
    chat_data["quiz_interval"] = interval
    await update_user(chat_id, chat_data)

    await message.reply_text(f"Quiz interval has been set to {interval} minutes for this group.")

# ... (keep the existing user management code)
