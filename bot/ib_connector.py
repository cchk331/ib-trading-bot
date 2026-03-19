import logging
from ib_insync import IB, Stock, Option, MarketOrder, LimitOrder
from bot.config import IB_HOST, IB_PORT, IB_CLIENT_ID, ACCOUNT_ID

logger = logging.getLogger(__name__)


class IBConnector:
    def __init__(self):
        self.ib = IB()
        self.connected = False

    def connect(self):
        try:
            self.ib.connect(IB_HOST, IB_PORT, clientId=IB_CLIENT_ID)
            self.connected = True
            logger.info(f"Connected to IB at {IB_HOST}:{IB_PORT}")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.connected = False

    def disconnect(self):
        if self.connected:
            self.ib.disconnect()
            self.connected = False

    def get_positions(self):
        return self.ib.positions()

    def get_portfolio(self):
        return self.ib.portfolio()

    def get_option_chain(self, symbol):
        stock = Stock(symbol, "SMART", "USD")
        self.ib.qualifyContracts(stock)
        chains = self.ib.reqSecDefOptParams(
            stock.symbol, "", stock.secType, stock.conId
        )
        return chains

    def place_market_order(self, contract, action, qty):
        order = MarketOrder(action, qty)
        trade = self.ib.placeOrder(contract, order)
        logger.info(f"{action} {qty} {contract.symbol}")
        return trade

    def place_limit_order(self, contract, action, qty, price):
        order = LimitOrder(action, qty, price)
        trade = self.ib.placeOrder(contract, order)
        logger.info(f"{action} {qty} {contract.symbol} @ {price}")
        return trade

    def cancel_order(self, trade):
        self.ib.cancelOrder(trade.order)

    def get_open_orders(self):
        return self.ib.openOrders()

    def get_historical_data(self, contract, duration="1 D", bar_size="5 mins"):
        return self.ib.reqHistoricalData(
            contract, endDateTime="",
            durationStr=duration, barSizeSetting=bar_size,
            whatToShow="MIDPOINT", useRTH=True,
        )

    def sleep(self, seconds=0):
        self.ib.sleep(seconds)
