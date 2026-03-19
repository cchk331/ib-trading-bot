import logging
import time
import os
import schedule
from datetime import datetime
from bot.config import LOG_LEVEL, LOG_FILE, MARKET_OPEN_HOUR, MARKET_OPEN_MIN, MARKET_CLOSE_HOUR, MARKET_CLOSE_MIN
from bot.ib_connector import IBConnector
from bot.strategy import SPXCreditSpreadStrategy
from bot.telegram_alerts import send_telegram, alert_error

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def is_market_hours():
    now = datetime.now()
    market_open = now.replace(hour=MARKET_OPEN_HOUR, minute=MARKET_OPEN_MIN, second=0)
    market_close = now.replace(hour=MARKET_CLOSE_HOUR, minute=MARKET_CLOSE_MIN, second=0)
    return market_open <= now <= market_close


def run_bot():
    logger.info("Starting IB Trading Bot...")
    send_telegram("Bot starting up")

    connector = IBConnector()
    connector.connect()

    if not connector.connected:
        alert_error("Failed to connect to IB Gateway")
        return

    strategy = SPXCreditSpreadStrategy(connector)

    try:
        while True:
            if is_market_hours():
                signal = strategy.execute()
                if signal:
                    logger.info(f"Executing signal: {signal}")
            else:
                logger.debug("Outside market hours")
            connector.sleep(30)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        alert_error(str(e))
        logger.exception("Bot crashed")
    finally:
        connector.disconnect()
        send_telegram("Bot shutting down")


if __name__ == "__main__":
    run_bot()
