from enum import Enum
import logging
import os
import json

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,ConversationHandler,
                          MessageHandler, filters, CallbackQueryHandler)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the bot token from the environment variable
bot_token = os.getenv('BOT_TOKEN')

# Определяем константы этапов разговора
MODULE_STEP, UNIT, AREA, YEAR_OF_CONSTRUCTION, FLAT_FLOOR, FLOORS_COUNT, WALL_TYPE, PRIVATE_DORM = range(8)

# Read JSON file
with open('data.json', 'r') as file:
    json_data = json.load(file)  # Parse JSON

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def start(update: Update, context) -> None:
    await update.message.reply_text(
        "Чем могу помочь ?\n"
        'Команда /cancel, чтобы прекратить разговор.\n\n'
        ,
        reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text=json_data[key]['description'], callback_data=key)] for key in json_data.keys()
            ])
        # ReplyKeyboardMarkup([reply_keyboard], one_time_keyboard=True)
    )
    return MODULE_STEP

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

# Обрабатываем модуль пользователя
async def module_step_handler(update, context):
    query = update.callback_query
    await query.answer()

    selected_module = query.data

    context.user_data["module"] = selected_module

    await query.message.reply_text(
        text = "Please select unit for " + selected_module, 
        reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text=json_data[selected_module]['units'][key]['title'], callback_data=key)] for key in json_data[selected_module]['units'].keys()
            ])
    )
    # переходим к этапу `Unit`
    return UNIT

# Обрабатываем unit пользователя
async def number_of_rooms_handler(update, context):
    context.user_json_data["units"] = update.message.text

    await update.message.reply_text('Please write appartment area')
    # переходим к этапу `LOCATION`
    return AREA

# Обрабатываем команду /cancel если пользователь отменил разговор
async def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    await update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END

def main():
    application = ApplicationBuilder().token(bot_token).build()
    
    conversation_handler = ConversationHandler(
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            MODULE_STEP: [CallbackQueryHandler(module_step_handler)],
            UNIT: [MessageHandler(filters.TEXT, number_of_rooms_handler)],
            # AREA: [
            #     MessageHandler(filters.TEXT, area_handler),
            # ],
            # YEAR_OF_CONSTRUCTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, year_of_construction_handler)],
            # FLAT_FLOOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, flat_floor_handler)],
            # FLOORS_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, floors_count_handler)],
            # WALL_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, wall_type_handler)],
            # PRIVATE_DORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, private_dorm_handler)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )


    application.add_handler(conversation_handler)
    # Обработчик на все случаи
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Register the error handler
    application.add_error_handler(error_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
