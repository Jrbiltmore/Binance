import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Strategy:
    def __init__(self, data_processor, execution, risk_management):
        """
        Initialize the Strategy with data processor, execution, and risk management instances.

        :param data_processor: Instance of DataProcessor for market data analysis
        :param execution: Instance of Execution for trade execution
        :param risk_management: Instance of RiskManagement for managing risk
        """
        self.data_processor = data_processor
        self.execution = execution
        self.risk_management = risk_management
        logger.info("Strategy initialized with data processor, execution, and risk management")

    def moving_average_strategy(self, symbol, short_window=40, long_window=100):
        """
        Implement a moving average crossover strategy.

        :param symbol: Trading symbol (e.g., 'BTCUSDT')
        :param short_window: Window size for short moving average
        :param long_window: Window size for long moving average
        """
        data = self.data_processor.fetch_data(symbol)
        data['short_mavg'] = data['close'].rolling(window=short_window).mean()
        data['long_mavg'] = data['close'].rolling(window=long_window).mean()
        data['signal'] = 0.0
        data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1.0, 0.0)
        data['positions'] = data['signal'].diff()

        logger.info(f"Generated signals for moving average strategy on {symbol}")

        for index, row in data.iterrows():
            if row['positions'] == 1.0:
                # Buy signal
                self.execution.place_order(symbol=symbol, quantity=1, order_type='market')
                logger.info(f"Buy signal for {symbol} at {row['close']}")
            elif row['positions'] == -1.0:
                # Sell signal
                self.execution.place_order(symbol=symbol, quantity=1, order_type='market')
                logger.info(f"Sell signal for {symbol} at {row['close']}")

    def rsi_strategy(self, symbol, window=14, overbought=70, oversold=30):
        """
        Implement a Relative Strength Index (RSI) strategy.

        :param symbol: Trading symbol (e.g., 'BTCUSDT')
        :param window: Window size for RSI calculation
        :param overbought: Overbought threshold for RSI
        :param oversold: Oversold threshold for RSI
        """
        data = self.data_processor.fetch_data(symbol)
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        data['signal'] = 0.0
        data['signal'] = np.where(data['RSI'] > overbought, -1.0, np.where(data['RSI'] < oversold, 1.0, 0.0))

        logger.info(f"Generated signals for RSI strategy on {symbol}")

        for index, row in data.iterrows():
            if row['signal'] == 1.0:
                # Buy signal
                self.execution.place_order(symbol=symbol, quantity=1, order_type='market')
                logger.info(f"Buy signal for {symbol} at {row['close']} (RSI: {row['RSI']})")
            elif row['signal'] == -1.0:
                # Sell signal
                self.execution.place_order(symbol=symbol, quantity=1, order_type='market')
                logger.info(f"Sell signal for {symbol} at {row['close']} (RSI: {row['RSI']})")

# Example usage:
if __name__ == "__main__":
    class MockDataProcessor:
        def fetch_data(self, symbol):
            dates = pd.date_range('2022-01-01', periods=200)
            data = pd.DataFrame(index=dates)
            data['close'] = np.random.randn(200).cumsum() + 100
            return data

    class MockExecution:
        def place_order(self, symbol, quantity, order_type='market', price=None):
            return {"symbol": symbol, "quantity": quantity, "type": order_type, "price": price, "status": "filled"}

    class MockRiskManagement:
        def manage_risk(self):
            pass

    data_processor = MockDataProcessor()
    execution = MockExecution()
    risk_management = MockRiskManagement()
    strategy = Strategy(data_processor, execution, risk_management)

    # Moving Average Strategy
    strategy.moving_average_strategy(symbol='BTCUSDT')

    # RSI Strategy
    strategy.rsi_strategy(symbol='BTCUSDT')
