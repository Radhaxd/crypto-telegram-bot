
import json
import random
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import save_quiz_score, get_leaderboard, get_user, update_user
from utils.logger import quiz_logger

# Load quiz questions from JSON file
try:
    with open('data/quiz_questions.json', 'r') as f:
        all_quiz_questions = json.load(f)
    quiz_logger.info(f"Loaded {len(all_quiz_questions)} quiz questions successfully.")
except FileNotFoundError:
    quiz_logger.error("Error: quiz_questions.json file not found. Please ensure the file exists in the 'data' directory.")
    all_quiz_questions = []
except json.JSONDecodeError:
    quiz_logger.error("Error: Invalid JSON in quiz_questions.json. Please check the file format.")
    all_quiz_questions = []

# Implement quiz rotation
quiz_questions = []
QUESTIONS_PER_ROTATION = 1000

def rotate_questions():
    global quiz_questions
    quiz_questions = random.sample(all_quiz_questions, min(QUESTIONS_PER_ROTATION, len(all_quiz_questions)))
    quiz_logger.info(f"Rotated {len(quiz_questions)} quiz questions.")

rotate_questions()  # Initial rotation

MAX_DAILY_QUIZZES = 50  # Set the maximum number of daily quizzes

async def send_quiz(client, chat_id):
    try:
        chat_data = await get_user(chat_id) or {"chat_id": chat_id}
        
        # Check daily quiz limit
        today = datetime.now().date()
        if chat_data.get('last_quiz_date') != str(today):
            chat_data['last_quiz_date'] = str(today)
            chat_data['daily_quiz_count'] = 0
        
        if chat_data.get('daily_quiz_count', 0) >= MAX_DAILY_QUIZZES:
            await client.send_message(chat_id, f"Daily quiz limit ({MAX_DAILY_QUIZZES}) reached. Try again tomorrow!")
            return

        if not quiz_questions:
            rotate_questions()

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
    except Exception as e:
        quiz_logger.error(f"Error in send_quiz for chat {chat_id}: {str(e)}", exc_info=True)

# ... (keep the rest of the quiz handler code, adding try-except blocks and logging where appropriate)

async def auto_quiz_task():
    while True:
        try:
            groups = await get_auto_quiz_groups()
            for group in groups:
                chat_data = await get_user(group['chat_id'])
                interval = chat_data.get('quiz_interval', 10)  # Default to 10 minutes if not set
                if (datetime.now() - chat_data.get('last_quiz_time', datetime.min)).total_seconds() >= interval * 60:
                    await send_quiz(Client, group['chat_id'])
                    chat_data['last_quiz_time'] = datetime.now()
                    await update_user(group['chat_id'], chat_data)
            await asyncio.sleep(60)  # Check every minute
        except Exception as e:
            quiz_logger.error(f"Error in auto_quiz_task: {str(e)}", exc_info=True)
            await asyncio.sleep(60)  # Wait a minute before retrying

# Rotate questions daily
async def daily_question_rotation():
    while True:
        await asyncio.sleep(24 * 60 * 60)  # Wait for 24 hours
        rotate_questions()

# Add this to your main bot file to start the daily rotation
# asyncio.create_task(daily_question_rotation())
