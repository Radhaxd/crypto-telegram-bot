
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import get_user, update_user
from config.config import config

ADMIN_USER_IDS = [12345678]  # Replace with actual admin user IDs

def is_admin(func):
    async def wrapper(client, message):
        if message.from_user.id not in ADMIN_USER_IDS:
            await message.reply_text("You don't have permission to use this command.")
            return
        return await func(client, message)
    return wrapper

@Client.on_message(filters.command("broadcast") & filters.user(ADMIN_USER_IDS))
@is_admin
async def broadcast_message(client, message):
    if len(message.text.split()) < 2:
        await message.reply_text("Please provide a message to broadcast.")
        return

    broadcast_message = message.text.split(None, 1)[1]
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Accept", callback_data="broadcast_accept"),
         InlineKeyboardButton("❌ Decline", callback_data="broadcast_decline")]
    ])

    # In a real scenario, you'd fetch all users from the database
    # For demonstration, we'll just send to the admin
    await client.send_message(
        chat_id=message.from_user.id,
        text=f"📢 Broadcast Message:\n\n{broadcast_message}",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("^broadcast_"))
async def handle_broadcast_response(client, callback_query):
    action = callback_query.data.split("_")[1]
    if action == "accept":
        await callback_query.answer("You've accepted the broadcast message.")
    else:
        await callback_query.answer("You've declined the broadcast message.")
    await callback_query.message.edit_text(f"You've {action}ed the broadcast message.")

@Client.on_message(filters.command(["mute", "ban", "warn"]) & filters.group)
@is_admin
async def moderate_user(client, message):
    if len(message.text.split()) < 2 or not message.reply_to_message:
        await message.reply_text("Please reply to a user's message with this command.")
        return

    action = message.text.split()[0][1:]  # Remove the '/' from the command
    user = message.reply_to_message.from_user
    chat = message.chat

    if action == "mute":
        await client.restrict_chat_member(chat.id, user.id, permissions=chat.permissions)
        await message.reply_text(f"{user.mention} has been muted.")
    elif action == "ban":
        await client.ban_chat_member(chat.id, user.id)
        await message.reply_text(f"{user.mention} has been banned.")
    elif action == "warn":
        # Implement a warning system here
        await message.reply_text(f"{user.mention} has been warned.")

@Client.on_message(filters.command(["enable", "disable"]) & filters.group & filters.user(ADMIN_USER_IDS))
@is_admin
async def toggle_feature(client, message):
    if len(message.text.split()) != 2:
        await message.reply_text("Please specify a feature to enable/disable.")
        return

    action, feature = message.text.split()
    action = action[1:]  # Remove the '/' from the command
    chat_id = message.chat.id

    # Update the chat settings in the database
    await update_user(chat_id, {f"feature_{feature}": action == "enable"})

    await message.reply_text(f"Feature '{feature}' has been {action}d for this chat.")
