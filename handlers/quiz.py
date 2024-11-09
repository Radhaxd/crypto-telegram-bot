
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import save_quiz_score, get_leaderboard
import random

quiz_questions = [
    {
        "question": "What is the maximum supply of Bitcoin?",
        "options": ["21 million", "18 million", "100 million", "1 billion"],
        "correct_answer": 0
    },
    {
        "question": "Which cryptocurrency is known as 'digital silver'?",
        "options": ["Ethereum", "Litecoin", "Ripple", "Dogecoin"],
        "correct_answer": 1
    },
    # Add more questions here
]

@Client.on_message(filters.command("quiz"))
async def start_quiz(client, message):
    question = random.choice(quiz_questions)
    options = question["options"]
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(option, callback_data=f"quiz_{i}_{question['correct_answer']}")]
        for i, option in enumerate(options)
    ])
    
    await message.reply_text(
        f"🧩 Crypto Quiz\n\n{question['question']}",
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
