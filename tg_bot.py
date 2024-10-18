from enum import Enum
import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters, CallbackQueryHandler)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

class Modules(Enum):
    Module_1 = "Module 1"
    Module_2 = "Module 2"
    Module_3 = "Module 3"
    Module_4 = "Module 4"
    Module_5 = "Module 5"

module_select = {
    Modules.Module_1.value: "To be professional today",
    Modules.Module_2.value: "Business organizations",
    Modules.Module_3.value: "Business meetings",
    Modules.Module_4.value: "Bussines corresponders",
}
# Load environment variables from .env file
load_dotenv()

# Access the bot token from the environment variable
bot_token = os.getenv('BOT_TOKEN')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def help_command(update: Update, context) -> None:
    await update.message.reply_text(
        "Чем могу помочь ?\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=value, callback_data=key)] for key, value in module_select.items()
        ])
    )

async def handle_module_choose(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == Modules.Module_1.value:
        module_1_select = {
            "unit_1": "unit 1",
            "unit_2": "unit 2",
            "unit_3": "unit 3",
            "unit_4": "unit 4",
        }
        await query.edit_message_text(
            text="Ты выбрал " + module_select[Modules.Module_1.value],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text=value, callback_data=key)] for key, value in module_1_select.items()
            ])
        )
    elif query.data == "unit_1":
        text = ("Personal and Professional Qualities of a Professional \n " + 
            "1. Read the following words paying attention to the pronunciation.\n " + 
            "Professionalism [pra'fel(a)n(a)iz(a)m], satisfaction [sætis' fakf(a)n], expectation [ekspek'ter/(a)n], attribute [ætribjut), competence [kompit(a)ns), conscientiousness [kon/tenfesnas], integrity [in'tegriti], appropriateness [a'praupriatnas], awkwardness ['o:kwadnas]."
        )
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=text
        )
    elif query.data == "unit_2":
        text = ("А это у нас UNIT 2 \n " )
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=text
        )
    else:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Что это : {query.data}"
        )
# Функция для обработки обычных сообщений
async def echo(update: Update, context) -> None:
    await update.message.reply_text(f"Вы написали: {update.message.text}. Я помогу вам с английским!")


# Error handler function
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to notify the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # Notify the user that something went wrong
    if isinstance(update, Update):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Произошла ошибка. Пожалуйста, попробуйте снова позже.")

def main():
    application = ApplicationBuilder().token(bot_token).build()
    
    application.add_handler(CommandHandler("start", help_command))
    application.add_handler(CallbackQueryHandler(handle_module_choose))

    # Обработчик ответов на тесты
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Register the error handler
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
