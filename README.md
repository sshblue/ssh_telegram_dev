# 🤖 Professional Contact Portal Bot

A multilingual Telegram bot designed to streamline professional communication and project management. Built with Python and Supabase for robust data management.

## ✨ Features

- 🌐 **Multilingual Support**
  - French 🇫🇷
  - English 🇬🇧
  - Russian 🇷🇺

- 💼 **Professional Services**
  - 🚀 Project Proposals
  - 💡 Technical Support
  - 📫 Direct Contact
  - ℹ️ About Section

- 🛡️ **Secure Data Management**
  - Supabase Integration
  - Project Request Tracking
  - Support Ticket System

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Telegram Bot Token
- Supabase Account

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/sshblue/ssh_telegram_dev.git
cd ssh_telegram_dev
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the bot**
```bash
python main.py
```

### 🐳 Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d --build
```

2. **View logs**
```bash
docker logs -f telegram_bot
```

3. **Stop the bot**
```bash
docker-compose down
```

## 🗄️ Database Structure

### Project Requests Table
```sql
- user_id (text)
- username (text)
- message (text)
- language (text)
- created_at (timestamp)
- status (text)
```

### Support Requests Table
```sql
- user_id (text)
- username (text)
- message (text)
- language (text)
- created_at (timestamp)
- status (text)
```

## 🛠️ Configuration

### Environment Variables
```env
# Telegram Configuration
TELEGRAM_TOKEN=your_telegram_token

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Identity Configuration
COMPANY_NAME=your_company_name
DEVELOPER_NAME=your_name
TELEGRAM_USERNAME=@your_username
```

## 📱 Bot Commands

- `/start` - Launch the bot and select language
- Use menu buttons for navigation:
  - 🚀 Project Proposals
  - 💡 Technical Support
  - ℹ️ About
  - 📫 Contact
  - 🌐 Change Language

## 🔄 Updates and Maintenance

### Update the Bot
```bash
git pull
docker-compose up -d --build
```

### View Logs
```bash
docker-compose logs -f
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, please use the following channels:
- Open an issue on GitHub
- Contact through Telegram: @sshblue
- Technical support through the bot itself

---
Made with ❤️ by ssh
