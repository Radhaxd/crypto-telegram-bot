
from pyrogram import Client, filters
from database.db import get_user_preferences, update_user_preferences
from utils.i18n import i18n
from utils.logger import main_logger

@Client.on_message(filters.command("settings"))
async def user_settings(client, message):
    try:
        user_id = message.from_user.id
        preferences = await get_user_preferences(user_id)
        
        lang = preferences.get('language', 'en')
        favorite_crypto = preferences.get('favorite_crypto', 'BTC')
        
        response = f"Your current settings:\n\n"
        response += f"Language: {lang}\n"
        response += f"Favorite Cryptocurrency: {favorite_crypto}\n\n"
        response += "Use /setlang [language_code] to change your language.\n"
        response += "Use /setfavorite [crypto_symbol] to set your favorite cryptocurrency."
        
        await message.reply_text(response)
    except Exception as e:
        main_logger.error(f"Error in user_settings: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while fetching your settings.")

@Client.on_message(filters.command("setlang"))
async def set_language(client, message):
    try:
        user_id = message.from_user.id
        preferences = await get_user_preferences(user_id)
        
        if len(message.text.split()) != 2:
            await message.reply_text("Usage: /setlang [language_code]")
            return
        
        lang = message.text.split()[1].lower()
        if lang not in i18n.translations:
            await message.reply_text("Unsupported language. Available languages: " + ", ".join(i18n.translations.keys()))
            return
        
        preferences['language'] = lang
        await update_user_preferences(user_id, preferences)
        
        await message.reply_text(i18n.get_text("language_set", lang))
    except Exception as e:
        main_logger.error(f"Error in set_language: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while setting your language.")

@Client.on_message(filters.command("setfavorite"))
async def set_favorite_crypto(client, message):
    try:
        user_id = message.from_user.id
        preferences = await get_user_preferences(user_id)
        
        if len(message.text.split()) != 2:
            await message.reply_text("Usage: /setfavorite [crypto_symbol]")
            return
        
        crypto = message.text.split()[1].upper()
        preferences['favorite_crypto'] = crypto
        await update_user_preferences(user_id, preferences)
        
        lang = preferences.get('language', 'en')
        await message.reply_text(i18n.get_text("favorite_crypto_set", lang, crypto=crypto))
    except Exception as e:
        main_logger.error(f"Error in set_favorite_crypto: {str(e)}", exc_info=True)
        await message.reply_text("An error occurred while setting your favorite cryptocurrency.")
