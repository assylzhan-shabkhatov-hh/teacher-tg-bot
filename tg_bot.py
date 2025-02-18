import json
import os

from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

# Load environment variables from .env file
load_dotenv()

# Access the bot token from the environment variable
bot_token = os.getenv('BOT_TOKEN')


def load_quiz_data():
    with open("quiz_data.json", "r") as file:
        return json.load(file)

quiz_data = load_quiz_data()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

user_progress = {}
user_scores = {}
user_data = {}


async def start_quiz(update: Update, context):
    user_id = update.message.from_user.id
    user_progress[user_id] = 0
    user_data[user_id] = {
        "username": update.message.from_user.username,
        "first_name": update.message.from_user.first_name,
        "last_name": update.message.from_user.last_name,
        "chat_id": update.message.chat.id
    }
    await send_question(update, update.message.from_user.id, update.message.chat.id)

async def send_question(update: Update, user_id, chat_id):
    index = user_progress.get(user_id, 0)
    if index < len(quiz_data["questions"]):
        question_data = quiz_data["questions"][index]
        buttons = [[KeyboardButton(text=option)] for option in question_data["options"]]
        keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text(question_data["question"], reply_markup=keyboard)
    else:
        print("Quiz already completed!", user_data[user_id])
        await update.message.reply_text("Quiz finished! 🎉")


async def check_answer(update: Update, context):
    user_id = update.message.from_user.id

    if(not user_id in user_data):
        await update.message.reply_text("Please start the quiz first using /quiz command.")
        return
    
    index = user_progress.get(user_id, 0)
    if index < len(quiz_data["questions"]):
        question_data = quiz_data["questions"][index]
        if update.message.text == question_data["options"][question_data["correct"]]:
            await update.message.reply_text("Correct! 🎉")
        else:
            await update.message.reply_text("Wrong answer. Try again! ❌")
            return
        if(user_id not in user_progress):
            user_progress[user_id] = 0
        user_progress[user_id] += 1
        await send_question(update, user_id, update.message.chat.id)
    else:
        await update.message.reply_text("Quiz already completed! ✅")

def main():
    application = ApplicationBuilder().token(bot_token).build()
    
    application.add_handler(CommandHandler("quiz", start_quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))  # Add this line

    application.run_polling()


if __name__ == '__main__':
    main()
