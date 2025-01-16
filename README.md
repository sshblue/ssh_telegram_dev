# Telegram Bot Portal

A professional contact portal bot for Telegram with multi-language support and Supabase integration.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`

3. Run the bot:
```bash
python main.py
```

## Docker Deployment

### Prerequisites
- Docker and Docker Compose installed on your VPS
- SSH access to your VPS

### Deployment Steps

1. Connect to your VPS:
```bash
ssh username@your_hostinger_vps_ip
```

2. Install Docker (if not already installed):
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

3. Install Docker Compose:
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

4. Clone the repository:
```bash
git clone <your-repo-url>
cd ssh_telegram_dev
```

5. Configure environment:
```bash
cp .env.example .env
nano .env  # Edit with your configuration
```

6. Build and start the container:
```bash
docker-compose up -d --build
```

### Maintenance Commands

- View logs:
```bash
docker-compose logs -f bot
```

- Restart the bot:
```bash
docker-compose restart bot
```

- Stop the bot:
```bash
docker-compose down
```

- Update the bot:
```bash
git pull
docker-compose up -d --build
```
