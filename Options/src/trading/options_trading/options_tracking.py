import pandas as pd
import numpy as np
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from retrying import retry
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptionsTracking:
    def __init__(self, api_key, api_secret):
        """
        Initialize the OptionsTracking with Binance API credentials.

        :param api_key: Binance API key
        :param api_secret: Binance API secret
        """
        self.client = Client(api_key, api_secret)
        logger.info("Binance client initialized for options tracking")

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def fetch_trade_history(self, symbol, start_time=None, end_time=None):
        """
        Fetch the trade history for a given symbol.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param start_time: Start time in milliseconds (optional)
        :param end_time: End time in milliseconds (optional)
        :return: DataFrame containing trade history
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            trades = self.client.get_my_trades(symbol=symbol, startTime=start_time, endTime=end_time)
            trade_history = pd.DataFrame(trades)
            trade_history['time'] = pd.to_datetime(trade_history['time'], unit='ms')
            logger.info(f"Fetched trade history for {symbol}")
            return trade_history
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching trade history for {symbol}: {e}")
            raise e

    def calculate_performance_metrics(self, trade_history):
        """
        Calculate performance metrics from the trade history.

        :param trade_history: DataFrame containing trade history
        :return: Dictionary with performance metrics
        """
        if trade_history.empty:
            logger.warning("Trade history is empty, cannot calculate performance metrics")
            return {}

        trade_history['price'] = trade_history['price'].astype(float)
        trade_history['qty'] = trade_history['qty'].astype(float)
        trade_history['quoteQty'] = trade_history['quoteQty'].astype(float)

        total_trades = len(trade_history)
        total_volume = trade_history['qty'].sum()
        average_price = trade_history['price'].mean()
        total_quote_qty = trade_history['quoteQty'].sum()

        metrics = {
            'total_trades': total_trades,
            'total_volume': total_volume,
            'average_price': average_price,
            'total_quote_qty': total_quote_qty
        }

        logger.info(f"Calculated performance metrics: {metrics}")
        return metrics

    def save_trade_history(self, trade_history, file_path):
        """
        Save trade history to a CSV file.

        :param trade_history: DataFrame containing trade history
        :param file_path: Path to the CSV file
        """
        try:
            trade_history.to_csv(file_path, index=False)
            logger.info(f"Trade history saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving trade history to {file_path}: {e}")
            raise e

# Example usage:
if __name__ == "__main__":
    api_key = 'your_api_key'
    api_secret = 'your_api_secret'
    tracker = OptionsTracking(api_key, api_secret)

    symbol = 'BTCUSDT'
    start_time = int(datetime(2021, 1, 1).timestamp() * 1000)
    end_time = int(datetime(2022, 1, 1).timestamp() * 1000)

    trade_history = tracker.fetch_trade_history(symbol, start_time, end_time)
    metrics = tracker.calculate_performance_metrics(trade_history)
    print(metrics)

    tracker.save_trade_history(trade_history, 'trade_history.csv')
