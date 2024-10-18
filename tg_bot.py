import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

# Load environment variables from .env file
load_dotenv()

# Access the bot token from the environment variable
bot_token = os.getenv('BOT_TOKEN')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def help_command(update: Update, context) -> None:
    await update.message.reply_text(
        "Чем могу помочь ?\n"
        "/1. To be professional today\n"
        "/2. Business organizations\n"
        "/3. Business meetings\n"
        "/4. Bussines corresponders\n"
    )

# Функция для команды /grammar
async def grammar(update: Update, context) -> None:
    await update.message.reply_text(
        "Вот некоторые важные грамматические правила:\n"
        "1. Present Simple используется для действий, происходящих регулярно.\n"
        "2. Present Continuous используется для действий, происходящих прямо сейчас."
    )

# Функция для команды /vocabulary
async def vocabulary(update: Update, context) -> None:
    await update.message.reply_text(
        "Сегодняшние новые слова:\n"
        "1. Apple - Яблоко\n"
        "2. Book - Книга\n"
        "3. Cat - Кот"
    )

# Функция для команды /quiz
async def quiz(update: Update, context) -> None:
    await update.message.reply_text(
        "Начнем небольшой тест:\n"
        "Какое время используется для описания действий, происходящих прямо сейчас?\n"
        "1. Present Simple\n"
        "2. Present Continuous\n"
        "Напишите ваш ответ (1 или 2)."
    )

# Функция для обработки ответов на тесты
async def handle_quiz_answer(update: Update, context) -> None:
    user_answer = update.message.text
    if user_answer == "2":
        await update.message.reply_text("Правильно! Present Continuous используется для действий, происходящих сейчас.")
    else:
        await update.message.reply_text("Неправильно. Правильный ответ: Present Continuous.")

# Функция для обработки обычных сообщений
async def echo(update: Update, context) -> None:
    await update.message.reply_text(f"Вы написали: {update.message.text}. Я помогу вам с английским!")


def main():
    application = ApplicationBuilder().token(bot_token).build()
    
    # start_handler = CommandHandler('start', start)
    # message_handler = MessageHandler(filters.TEXT, handle_message)

    # application.add_handler(start_handler)
    # application.add_handler(message_handler)
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CommandHandler("1", grammar))
    application.add_handler(CommandHandler("2", vocabulary))
    application.add_handler(CommandHandler("3", quiz))

    # Обработчик ответов на тесты
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quiz_answer))
    
    application.run_polling()


if __name__ == '__main__':
    main()
