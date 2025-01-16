import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters, ConversationHandler
from config import TELEGRAM_TOKEN, LANGUAGE_SELECT_MESSAGE, MESSAGES
from database import save_project_request, save_support_request

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# États de conversation
WAITING_FOR_PROJECT = 1
WAITING_FOR_SUPPORT = 2

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire de la commande /start"""
    keyboard = [
        [
            InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr'),
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(LANGUAGE_SELECT_MESSAGE, reply_markup=reply_markup, parse_mode='HTML')

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, language='fr'):
    """Affiche le menu principal dans la langue sélectionnée"""
    messages = MESSAGES[language]
    keyboard = [
        [
            InlineKeyboardButton(f"🚀 {messages['menu']['project']}", callback_data=f'{language}_project'),
            InlineKeyboardButton(f"💡 {messages['menu']['support']}", callback_data=f'{language}_support')
        ],
        [
            InlineKeyboardButton(f"ℹ️ {messages['menu']['about']}", callback_data=f'{language}_about'),
            InlineKeyboardButton(f"📫 {messages['menu']['contact']}", callback_data=f'{language}_contact')
        ],
        [
            InlineKeyboardButton(f"🌐 {messages['menu']['change_lang']}", callback_data='change_lang')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.message.edit_text(messages['welcome'], reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(messages['welcome'], reply_markup=reply_markup, parse_mode='HTML')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire des callbacks des boutons"""
    query = update.callback_query
    await query.answer()

    if query.data.startswith('lang_'):
        language = query.data.split('_')[1]
        await show_main_menu(update, context, language)
        context.user_data['language'] = language
    elif query.data == 'change_lang':
        keyboard = [
            [
                InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr'),
                InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
                InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(LANGUAGE_SELECT_MESSAGE, reply_markup=reply_markup, parse_mode='HTML')
    else:
        language, action = query.data.split('_')
        messages = MESSAGES[language]
        if action == 'about':
            await query.message.reply_text(messages['about'], parse_mode='HTML')
        elif action == 'project':
            await query.message.reply_text(messages['project_prompt'], parse_mode='HTML')
            context.user_data['waiting_for'] = 'project'
        elif action == 'support':
            await query.message.reply_text(messages['support_prompt'], parse_mode='HTML')
            context.user_data['waiting_for'] = 'support'
        elif action == 'contact':
            await query.message.reply_text(messages['contact'], parse_mode='HTML')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire des messages texte"""
    user_message = update.message.text
    user_name = update.message.from_user.username or update.message.from_user.first_name
    user_id = update.message.from_user.id
    language = context.user_data.get('language', 'fr')
    
    # Vérifier l'état de la conversation
    if context.user_data.get('waiting_for') == 'project':
        # Sauvegarder la demande de projet
        await save_project_request(user_id, user_name, user_message, language)
        await update.message.reply_text(MESSAGES[language]['message_received'], parse_mode='HTML')
        context.user_data.pop('waiting_for', None)
        return ConversationHandler.END
        
    elif context.user_data.get('waiting_for') == 'support':
        # Sauvegarder la demande de support
        await save_support_request(user_id, user_name, user_message, language)
        await update.message.reply_text(MESSAGES[language]['message_received'], parse_mode='HTML')
        context.user_data.pop('waiting_for', None)
        return ConversationHandler.END
    
    logging.info(f"Message reçu de {user_name} (ID: {user_id}): {user_message}")
    await update.message.reply_text(MESSAGES[language]['message_received'], parse_mode='HTML')

def main():
    """Fonction principale du bot"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            WAITING_FOR_PROJECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
            WAITING_FOR_SUPPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)]
        },
        fallbacks=[]
    ))

    application.run_polling()

if __name__ == '__main__':
    main()
