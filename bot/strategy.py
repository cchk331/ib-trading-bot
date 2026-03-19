import logging
from datetime import datetime
from ib_insync import Option
from bot.config import MAX_POSITION_SIZE, MAX_DAILY_LOSS

logger = logging.getLogger(__name__)


class BaseStrategy:
    def __init__(self, connector):
        self.connector = connector
        self.daily_pnl = 0.0
        self.positions_today = 0

    def check_risk_limits(self):
        if abs(self.daily_pnl) >= MAX_DAILY_LOSS:
            logger.warning(f"Daily loss limit hit: {self.daily_pnl}")
            return False
        if self.positions_today >= MAX_POSITION_SIZE:
            logger.warning("Max position size reached")
            return False
        return True

    def evaluate_signal(self):
        raise NotImplementedError

    def execute(self):
        if not self.check_risk_limits():
            return None
        signal = self.evaluate_signal()
        if signal:
            logger.info(f"Signal: {signal}")
        return signal


class SPXCreditSpreadStrategy(BaseStrategy):
    def __init__(self, connector, symbol="SPX", delta_target=0.10):
        super().__init__(connector)
        self.symbol = symbol
        self.delta_target = delta_target

    def evaluate_signal(self):
        now = datetime.now()
        if now.hour < 10 or now.hour >= 15:
            return None
        logger.info("Evaluating 0DTE credit spread...")
        # TODO: Implement your 0DTE logic here
        # 1. Get SPX price
        # 2. Get 0DTE option chain
        # 3. Find strikes near delta_target
        # 4. Check RSI, MACD, Stochastic RSI
        # 5. Return signal if conditions met
        return None
