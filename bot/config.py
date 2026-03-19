import os
from dotenv import load_dotenv

load_dotenv()

# IB Gateway settings
IB_HOST = os.getenv("IB_HOST", "127.0.0.1")
IB_PORT = int(os.getenv("IB_PORT", 4002))  # 4001=live, 4002=paper
IB_CLIENT_ID = int(os.getenv("IB_CLIENT_ID", 1))

# Trading settings
ACCOUNT_ID = os.getenv("ACCOUNT_ID", "")
MAX_POSITION_SIZE = int(os.getenv("MAX_POSITION_SIZE", 1))
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", 500.0))

# Telegram alerts
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Market hours (ET)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MIN = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MIN = 0

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/trading_bot.log")
