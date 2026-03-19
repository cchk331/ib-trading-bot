import logging
import requests
from bot.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Telegram send failed: {e}")


def alert_trade(action, symbol, qty, price=None):
    msg = f"TRADE: {action} {qty}x {symbol}"
    if price:
        msg += f" @ ${price}"
    send_telegram(msg)


def alert_error(error_msg):
    send_telegram(f"ERROR: {error_msg}")


def alert_daily_summary(pnl, trades_count):
    send_telegram(f"DAILY: PnL=${pnl:.2f} Trades={trades_count}")
