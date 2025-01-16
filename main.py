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
        # Create language selection keyboard with emojis and better formatting
        keyboard = [
            [
                InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr'),
                InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
                InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🌍 Choisissez votre langue / Choose your language / Выберите язык:",
            reply_markup=reply_markup
        )
        return

    # Get messages for user's language
    messages = MESSAGES[context.user_data['language']]
    
    # Create main menu keyboard with emojis
    keyboard = [
        [InlineKeyboardButton(f"🚀 {messages['menu']['project']}", callback_data='project')],
        [InlineKeyboardButton(f"💡 {messages['menu']['support']}", callback_data='support')],
        [InlineKeyboardButton(f"ℹ️ {messages['menu']['about']}", callback_data='about')],
        [InlineKeyboardButton(f"📫 {messages['menu']['contact']}", callback_data='contact')],
        [InlineKeyboardButton(f"🌍 {messages['menu']['change_lang']}", callback_data='change_lang')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
🤖 {messages['welcome']}
"""
    await update.message.reply_text(
        welcome_message,
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
        if language in MESSAGES:  # Vérifier que la langue est valide
            context.user_data['language'] = language
            # Show main menu after language selection
            await start(update, context)
        else:
            print(f"Warning: Invalid language selection: {language}")
        return
    
    if query.data == 'change_lang':
        # Show language selection menu with better formatting
        keyboard = [
            [
                InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr'),
                InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
                InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🌍 Choisissez votre langue / Choose your language / Выберите язык:",
            reply_markup=reply_markup
        )
        return
    
    # Get messages for user's language
    messages = MESSAGES[context.user_data['language']]
    
    if query.data == 'project':
        context.user_data['action'] = 'project'
        project_message = f"""
🚀 {messages['project_prompt']}

✨ Tips:
• Décrivez votre projet en détail
• Mentionnez vos contraintes techniques
• Indiquez vos délais souhaités
"""
        await query.edit_message_text(
            text=project_message,
            parse_mode='HTML'
        )
    elif query.data == 'support':
        context.user_data['action'] = 'support'
        support_message = f"""
💡 {messages['support_prompt']}

✨ Tips:
• Décrivez votre problème précisément
• Partagez les messages d'erreur si possible
• Indiquez l'urgence de votre demande
"""
        await query.edit_message_text(
            text=support_message,
            parse_mode='HTML'
        )
    elif query.data == 'about':
        about_message = f"""
ℹ️ {messages['about']}

🌟 Nos services:
• Développement sur mesure
• Support technique
• Conseil en innovation
"""
        keyboard = [[InlineKeyboardButton(f"🚀 {messages['menu']['project']}", callback_data='project')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=about_message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    elif query.data == 'contact':
        contact_message = f"""
📫 {messages['contact']}

📱 Réseaux sociaux:
• Twitter: @sshblue
• LinkedIn: SSHBlue
• GitHub: sshblue
"""
        await query.edit_message_text(
            text=contact_message,
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
            success_message = f"""
✅ {messages['message_received']}

🎉 Merci pour votre demande de projet !
⏳ Notre équipe vous contactera très bientôt.
"""
            await update.message.reply_text(
                success_message,
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Error saving project request: {e}")
            await update.message.reply_text(
                "❌ Une erreur s'est produite. Veuillez réessayer plus tard.",
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
            success_message = f"""
✅ {messages['message_received']}

🎯 Votre demande de support a été enregistrée !
⚡ Notre équipe technique va l'examiner rapidement.
"""
            await update.message.reply_text(
                success_message,
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Error saving support request: {e}")
            await update.message.reply_text(
                "❌ Une erreur s'est produite. Veuillez réessayer plus tard.",
                parse_mode='HTML'
            )
    
    # Clear the action after handling
    context.user_data['action'] = None

def main():
    """Start the bot."""
    print("🤖 Démarrage du bot...")
    
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    print("✨ Bot prêt à recevoir des messages !")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
