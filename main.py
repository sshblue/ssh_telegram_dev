import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from dotenv import load_dotenv
from database import save_project_request, save_support_request
from config import FR_MESSAGES, EN_MESSAGES, RU_MESSAGES, MESSAGES

# Load environment variables
load_dotenv()

# Get bot token from environment variable
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    if not context.user_data.get('language'):
        # Create language selection keyboard
        keyboard = [
            [
                InlineKeyboardButton("Français ", callback_data='lang_fr'),
                InlineKeyboardButton("English ", callback_data='lang_en'),
                InlineKeyboardButton("", callback_data='lang_ru')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=" Выберите язык / Choose your language / Choisissez votre langue:",
            reply_markup=reply_markup
        )
        return

    # Get messages for user's language
    messages = MESSAGES[context.user_data['language']]
    
    # Create main menu keyboard
    keyboard = [
        [InlineKeyboardButton(messages['menu']['project'], callback_data='project')],
        [InlineKeyboardButton(messages['menu']['support'], callback_data='support')],
        [InlineKeyboardButton(messages['menu']['about'], callback_data='about')],
        [InlineKeyboardButton(messages['menu']['contact'], callback_data='contact')],
        [InlineKeyboardButton(messages['menu']['change_lang'], callback_data='change_lang')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages['welcome'],
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('lang_'):
        # Handle language selection
        language = query.data.split('_')[1]
        context.user_data['language'] = language
        
        # Show main menu after language selection
        await start(update, context)
        return
    
    if query.data == 'change_lang':
        # Show language selection menu
        keyboard = [
            [
                InlineKeyboardButton("Français ", callback_data='lang_fr'),
                InlineKeyboardButton("English ", callback_data='lang_en'),
                InlineKeyboardButton("", callback_data='lang_ru')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=" Выберите язык / Choose your language / Choisissez votre langue:",
            reply_markup=reply_markup
        )
        return
    
    # Get messages for user's language
    messages = MESSAGES[context.user_data['language']]
    
    if query.data == 'project':
        context.user_data['action'] = 'project'
        await query.edit_message_text(
            text=messages['project_prompt'],
            parse_mode='HTML'
        )
    elif query.data == 'support':
        context.user_data['action'] = 'support'
        await query.edit_message_text(
            text=messages['support_prompt'],
            parse_mode='HTML'
        )
    elif query.data == 'about':
        keyboard = [[InlineKeyboardButton(messages['menu']['project'], callback_data='project')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=messages['about'],
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    elif query.data == 'contact':
        await query.edit_message_text(
            text=messages['contact'],
            parse_mode='HTML'
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages."""
    if not context.user_data.get('language'):
        # If no language is set, trigger start command
        await start(update, context)
        return
    
    messages = MESSAGES[context.user_data['language']]
    action = context.user_data.get('action')
    
    if action == 'project':
        try:
            save_project_request(
                user_id=update.message.from_user.id,
                username=update.message.from_user.username or "Anonymous",
                message=update.message.text,
                language=context.user_data['language']
            )
            await update.message.reply_text(
                messages['message_received'],
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Error saving project request: {e}")
            await update.message.reply_text(
                "An error occurred while saving your request. Please try again later.",
                parse_mode='HTML'
            )
    
    elif action == 'support':
        try:
            save_support_request(
                user_id=update.message.from_user.id,
                username=update.message.from_user.username or "Anonymous",
                message=update.message.text,
                language=context.user_data['language']
            )
            await update.message.reply_text(
                messages['message_received'],
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Error saving support request: {e}")
            await update.message.reply_text(
                "An error occurred while saving your request. Please try again later.",
                parse_mode='HTML'
            )
    
    # Clear the action after handling
    context.user_data['action'] = None

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    print("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
