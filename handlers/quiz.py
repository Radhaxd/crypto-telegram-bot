
import json
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import save_quiz_score, get_leaderboard, get_user, update_user

# Load quiz questions from JSON file
with open('data/quiz_questions.json', 'r') as f:
    quiz_questions = json.load(f)

@Client.on_message(filters.command("quiz"))
async def start_quiz(client, message):
    await send_quiz(client, message.chat.id)

async def send_quiz(client, chat_id):
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

@Client.on_callback_query(filters.regex("^quiz_"))
async def handle_quiz_answer(client, callback_query):
    _, selected_answer, correct_answer = callback_query.data.split("_")
    selected_answer = int(selected_answer)
    correct_answer = int(correct_answer)
    
    if selected_answer == correct_answer:
        response = "✅ Correct! Well done!"
        await save_quiz_score(callback_query.from_user.id, 1)
    else:
        response = f"❌ Oops! The correct answer was: {quiz_questions[0]['options'][correct_answer]}"
    
    await callback_query.answer(response, show_alert=True)
    await callback_query.message.reply_text(response)

@Client.on_message(filters.command("leaderboard"))
async def show_leaderboard(client, message):
    leaderboard = await get_leaderboard()
    
    if not leaderboard:
        await message.reply_text("No quiz scores recorded yet!")
        return
    
    response = "🏆 Crypto Quiz Leaderboard 🏆\n\n"
    for i, entry in enumerate(leaderboard, 1):
        response += f"{i}. User {entry['user_id']}: {entry['score']} points\n"
    
    await message.reply_text(response)

@Client.on_message(filters.command(["enable_quiz", "disable_quiz"]) & filters.group)
async def toggle_auto_quiz(client, message):
    chat_id = message.chat.id
    action = message.text.split()[0][1:].split('_')[0]  # 'enable' or 'disable'
    
    chat_data = await get_user(chat_id)
    if not chat_data:
        chat_data = {"chat_id": chat_id}
    
    chat_data["auto_quiz_enabled"] = (action == "enable")
    await update_user(chat_id, chat_data)
    
    await message.reply_text(f"Auto quiz has been {action}d for this group.")

async def auto_quiz_task():
    while True:
        # In a real scenario, you'd fetch all groups with auto_quiz_enabled from the database
        # For demonstration, we'll use a dummy group ID
        group_id = -1001234567890
        await send_quiz(Client, group_id)
        await asyncio.sleep(600)  # Wait for 10 minutes

# Add this to your main bot file to start the auto quiz task
# asyncio.create_task(auto_quiz_task())
