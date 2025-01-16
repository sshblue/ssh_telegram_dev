import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du bot
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Configuration de l'identité
COMPANY_NAME = os.getenv('COMPANY_NAME', 'ssh_blue')
DEVELOPER_NAME = os.getenv('DEVELOPER_NAME', 'ssh')
TELEGRAM_USERNAME = os.getenv('TELEGRAM_USERNAME', '@sshblue')

# Français (FR)
FR_MESSAGES = {
    'welcome': f"""
👋 Bienvenue sur le portail <b>{COMPANY_NAME}</b> !


Je suis votre assistant virtuel pour :

<i>🚀 Proposer des idées de projets</i>
<i>💡 Demander du support technique</i>
<i>📫 Contacter <b>{COMPANY_NAME}</b> directement</i>


Comment puis-je vous aider aujourd'hui ?
""",
    'about': f"""
À propos de <b>{COMPANY_NAME}</b> :


👨‍💻 <b>Développeur passionné</b>

🛠️ <b>Expert en développement logiciel</b>, <i>spécialisé dans les réseaux</i> (DNS, DHCP, etc.),

🤖 <b>Spécialisé dans les bots</b> (<i>Telegram</i>, <i>Discord</i>, etc.)

🌟 <b>Spécialisé dans la création de solutions privées</b>


<i>N'hésitez pas à me contacter pour vos projets !</i>
""",
    'project_prompt': """🚀 <b>Super !</b> Pour proposer un projet, décrivez-le moi en quelques lignes.

N'oubliez pas de mentionner :
- L'objectif principal
- Les fonctionnalités souhaitées
- Le délai envisagé""",
    'support_prompt': """💡 Pour toute question technique, décrivez votre problème en détail.
Je vous répondrai dans les plus brefs délais.""",
    'contact': f"""📫 <b>Vous pouvez me contacter directement</b> :
Telegram : {TELEGRAM_USERNAME}
<i>Je réponds généralement sous 24-48h.</i>""",
    'message_received': """<b>J'ai bien reçu votre message</b>. Je vous répondrai dans les plus brefs délais.

<i>En attendant, n'hésitez pas à explorer les autres options du menu principal avec /start</i>""",
    'menu': {
        'project': "Proposer un projet",
        'support': "Support technique",
        'about': "À propos",
        'contact': "Contact",
        'change_lang': "Changer de langue"
    }
}

# English (EN)
EN_MESSAGES = {
    'welcome': f"""
👋 Welcome to the <b>{COMPANY_NAME}</b> portal!


I am your virtual assistant for:

<i>🚀 Proposing project ideas</i>
<i>💡 Getting technical support</i>
<i>📫 Contacting <b>{COMPANY_NAME}</b> directly</i>


How can I help you today?
""",
    'about': f"""
About <b>{COMPANY_NAME}</b>:


👨‍💻 <b>Passionate Developer</b>

🛠️ <b>Software Development Expert</b>, <i>specialized in networking</i> (DNS, DHCP, etc.),

🤖 <b>Bot Development Specialist</b> (<i>Telegram</i>, <i>Discord</i>, etc.)

🌟 <b>Specialized in private services solutions</b>


<i>Feel free to contact me for your projects!</i>
""",
    'project_prompt': """🚀 <b>Great!</b> To propose a project, please describe it in a few lines.

Don't forget to mention:
- The main objective
- Desired features
- Expected timeline""",
    'support_prompt': """💡 For any technical question, please describe your issue in detail.
I will respond as soon as possible.""",
    'contact': f"""📫 <b>You can contact me directly</b>:
Telegram: {TELEGRAM_USERNAME}
<i>I usually respond within 24-48h.</i>""",
    'message_received': """<b>I have received your message</b>. I will respond as soon as possible.

<i>In the meantime, feel free to explore other options in the main menu with /start</i>""",
    'menu': {
        'project': "Propose a project",
        'support': "Technical support",
        'about': "About",
        'contact': "Contact",
        'change_lang': "Change language"
    }
}

# Russian (RU)
RU_MESSAGES = {
    'welcome': f"""
👋 Добро пожаловать на портал <b>{COMPANY_NAME}</b>!


Я ваш виртуальный помощник для:

<i>🚀 Предложения идей проектов</i>
<i>💡 Получения технической поддержки</i>
<i>📫 Прямого контакта с <b>{COMPANY_NAME}</b></i>


Как я могу помочь вам сегодня?
""",
    'about': f"""
О <b>{COMPANY_NAME}</b>:


👨‍💻 <b>Увлеченный разработчик</b>

🛠️ <b>Эксперт по разработке ПО</b>, <i>специализация в сетях</i> (DNS, DHCP и т.д.),

🤖 <b>Специалист по ботам</b> (<i>Telegram</i>, <i>Discord</i> и др.)

🌟 <b>Специализируюсь на частных решениях</b>


<i>Не стесняйтесь обращаться со своими проектами!</i>
""",
    'project_prompt': """🚀 <b>Отлично!</b> Для предложения проекта, опишите его в нескольких строках.

Не забудьте указать:
- Основную цель
- Желаемые функции
- Ожидаемые сроки""",
    'support_prompt': """💡 Для технических вопросов, пожалуйста, подробно опишите вашу проблему.
Я отвечу в кратчайшие сроки.""",
    'contact': f"""📫 <b>Вы можете связаться со мной напрямую</b>:
Telegram: {TELEGRAM_USERNAME}
<i>Обычно я отвечаю в течение 24-48 часов.</i>""",
    'message_received': """<b>Я получил ваше сообщение</b>. Отвечу в ближайшее время.

<i>Пока что вы можете изучить другие опции в главном меню с помощью /start</i>""",
    'menu': {
        'project': "Предложить проект",
        'support': "Техподдержка",
        'about': "О нас",
        'contact': "Контакт",
        'change_lang': "Сменить язык"
    }
}

# Message de sélection de langue
LANGUAGE_SELECT_MESSAGE = """
🌐 Выберите язык / Choose your language / Choisissez votre langue:
"""

# Mapping des langues
MESSAGES = {
    'fr': FR_MESSAGES,
    'en': EN_MESSAGES,
    'ru': RU_MESSAGES
}
