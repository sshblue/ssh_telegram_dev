import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext
)
from config import (
    TELEGRAM_TOKEN,
    FR_MESSAGES,
    EN_MESSAGES,
    RU_MESSAGES,
    LANGUAGE_SELECT_MESSAGE,
    MESSAGES
)
from database import save_project_request, save_support_request

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Vérification du token au démarrage
if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN n'est pas défini dans les variables d'environnement!")
    exit(1)

logger.info(f"Token length: {len(TELEGRAM_TOKEN)}")
logger.info("Starting bot...")

# States
SELECTING_LANGUAGE = 0
SELECTING_ACTION = 1
TYPING_PROJECT = 2
TYPING_SUPPORT = 3

def start(update: Update, context: CallbackContext) -> int:
    keyboard = [['🇫🇷 Français', '🇬🇧 English', '🇷🇺 Русский']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    update.message.reply_text(
        LANGUAGE_SELECT_MESSAGE,
        reply_markup=reply_markup
    )
    return SELECTING_LANGUAGE

def select_language(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if '🇫🇷' in text:
        context.user_data['language'] = 'fr'
    elif '🇬🇧' in text:
        context.user_data['language'] = 'en'
    elif '🇷🇺' in text:
        context.user_data['language'] = 'ru'
    else:
        return SELECTING_LANGUAGE

    messages = MESSAGES[context.user_data['language']]
    keyboard = [
        [messages['menu']['project'], messages['menu']['support']],
        [messages['menu']['about'], messages['menu']['contact']],
        [messages['menu']['change_lang']]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    update.message.reply_text(
        messages['welcome'],
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    return SELECTING_ACTION

def handle_action(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    language = context.user_data.get('language', 'en')
    messages = MESSAGES[language]

    if text == messages['menu']['project']:
        update.message.reply_text(
            messages['project_prompt'],
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove()
        )
        return TYPING_PROJECT
    elif text == messages['menu']['support']:
        update.message.reply_text(
            messages['support_prompt'],
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove()
        )
        return TYPING_SUPPORT
    elif text == messages['menu']['about']:
        update.message.reply_text(
            messages['about'],
            parse_mode='HTML'
        )
        return SELECTING_ACTION
    elif text == messages['menu']['contact']:
        update.message.reply_text(
            messages['contact'],
            parse_mode='HTML'
        )
        return SELECTING_ACTION
    elif text == messages['menu']['change_lang']:
        return start(update, context)
    
    return SELECTING_ACTION

def handle_project_message(update: Update, context: CallbackContext) -> int:
    language = context.user_data.get('language', 'en')
    messages = MESSAGES[language]
    
    save_project_request(
        user_id=str(update.message.from_user.id),
        username=update.message.from_user.username or "Unknown",
        message=update.message.text,
        language=language
    )
    
    keyboard = [
        [messages['menu']['project'], messages['menu']['support']],
        [messages['menu']['about'], messages['menu']['contact']],
        [messages['menu']['change_lang']]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    update.message.reply_text(
        messages['message_received'],
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    return SELECTING_ACTION

def handle_support_message(update: Update, context: CallbackContext) -> int:
    language = context.user_data.get('language', 'en')
    messages = MESSAGES[language]
    
    save_support_request(
        user_id=str(update.message.from_user.id),
        username=update.message.from_user.username or "Unknown",
        message=update.message.text,
        language=language
    )
    
    keyboard = [
        [messages['menu']['project'], messages['menu']['support']],
        [messages['menu']['about'], messages['menu']['contact']],
        [messages['menu']['change_lang']]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    update.message.reply_text(
        messages['message_received'],
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    return SELECTING_ACTION

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, select_language)],
            SELECTING_ACTION: [MessageHandler(Filters.text & ~Filters.command, handle_action)],
            TYPING_PROJECT: [MessageHandler(Filters.text & ~Filters.command, handle_project_message)],
            TYPING_SUPPORT: [MessageHandler(Filters.text & ~Filters.command, handle_support_message)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
