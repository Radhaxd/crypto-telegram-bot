
import json
import random
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import save_quiz_score, get_leaderboard, get_user, update_user

# ... (keep the existing quiz loading code)

MAX_DAILY_QUIZZES = 50  # Set the maximum number of daily quizzes

async def send_quiz(client, chat_id):
    chat_data = await get_user(chat_id) or {"chat_id": chat_id}
    
    # Check daily quiz limit
    today = datetime.now().date()
    if chat_data.get('last_quiz_date') != str(today):
        chat_data['last_quiz_date'] = str(today)
        chat_data['daily_quiz_count'] = 0
    
    if chat_data.get('daily_quiz_count', 0) >= MAX_DAILY_QUIZZES:
        await client.send_message(chat_id, f"Daily quiz limit ({MAX_DAILY_QUIZZES}) reached. Try again tomorrow!")
        return

    question = random.choice(quiz_questions)
    options = question["options"]
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(option, callback_data=f"quiz_{i}_{question['correct_answer']}")]
        for i, option in enumerate(options)
    ])
    
    await client.send_message(
        chat_id=chat_id,
        text=f"🧩 Crypto Quiz\n\n{question['question']}",
        reply_markup=keyboard
    )

    chat_data['daily_quiz_count'] = chat_data.get('daily_quiz_count', 0) + 1
    await update_user(chat_id, chat_data)

# ... (keep the existing quiz handler code)

async def auto_quiz_task():
    while True:
        groups = await get_auto_quiz_groups()
        for group in groups:
            chat_data = await get_user(group['chat_id'])
            interval = chat_data.get('quiz_interval', 10)  # Default to 10 minutes if not set
            if (datetime.now() - chat_data.get('last_quiz_time', datetime.min)).total_seconds() >= interval * 60:
                await send_quiz(Client, group['chat_id'])
                chat_data['last_quiz_time'] = datetime.now()
                await update_user(group['chat_id'], chat_data)
        await asyncio.sleep(60)  # Check every minute

# ... (keep the rest of the quiz handler code)
