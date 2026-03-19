# IB Trading Bot

Automated trading bot using Interactive Brokers API, developed in GitHub Codespaces and deployed to Oracle Cloud free tier VM.

## Architecture

```
GitHub Codespaces (dev) -> GitHub Actions (CI/CD) -> Oracle VM (production)
                                                      |- IB Gateway + IBC
                                                      |- Python trading bot
                                                      |- Telegram alerts
```

## Project Structure

```
ib-trading-bot/
|- .devcontainer/       # Codespaces config
|- .github/workflows/   # CI/CD deploy pipeline
|- bot/
|  |- main.py           # Entry point
|  |- config.py         # Environment config
|  |- ib_connector.py   # IB API wrapper
|  |- strategy.py       # Trading strategies
|  |- telegram_alerts.py # Notifications
|- scripts/
|  |- setup_oracle_vm.sh    # VM setup script
|  |- trading_bot.service   # systemd service
|- .env.example
|- requirements.txt
```

## Quick Start

### 1. Development (Codespaces)

1. Click **Code** > **Codespaces** > **Create codespace on main**
2. Copy `.env.example` to `.env` and fill in your values
3. Run: `python -m bot.main`

### 2. Oracle VM Setup

```bash
# SSH into your Oracle VM
ssh ubuntu@YOUR_VM_IP

# Clone the repo
git clone https://github.com/cchk331/ib-trading-bot.git
cd ib-trading-bot

# Run setup script
chmod +x scripts/setup_oracle_vm.sh
./scripts/setup_oracle_vm.sh

# Configure
cp .env.example .env
nano .env  # Fill in your values
nano ~/ibc/config.ini  # Add IB credentials

# Start
sudo systemctl start trading_bot
sudo systemctl status trading_bot
```

### 3. CI/CD Setup

Add these secrets in GitHub repo Settings > Secrets:
- `ORACLE_VM_HOST` - Your VM public IP
- `ORACLE_VM_USER` - SSH username (ubuntu)
- `ORACLE_VM_SSH_KEY` - Your private SSH key

### 4. Telegram Alerts Setup

1. Message @BotFather on Telegram, create a bot
2. Get the bot token
3. Send a message to your bot, then get chat_id from:
   `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
4. Add both to `.env`

## Key Commands

```bash
# Check bot status
sudo systemctl status trading_bot

# View logs
journalctl -u trading_bot -f
tail -f logs/trading_bot.log

# Restart bot
sudo systemctl restart trading_bot

# Start IB Gateway
~/start_ib_gateway.sh
```
