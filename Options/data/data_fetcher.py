from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import logging
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, api_key, api_secret):
        """
        Initialize the DataFetcher with Binance API credentials.

        :param api_key: Binance API key
        :param api_secret: Binance API secret
        """
        self.client = Client(api_key, api_secret)
        logger.info("Binance client initialized")

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_historical_data(self, symbol, interval, start_str, end_str=None):
        """
        Fetch historical market data for a given symbol and interval.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param interval: The interval for candlesticks, e.g., Client.KLINE_INTERVAL_1HOUR
        :param start_str: The start date string in '1 Dec, 2021' format
        :param end_str: The end date string in '1 Jan, 2022' format (optional)
        :return: A list of candlestick data
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            klines = self.client.get_historical_klines(symbol, interval, start_str, end_str)
            logger.info(f"Fetched historical data for {symbol} from {start_str} to {end_str}")
            return klines
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_current_price(self, symbol):
        """
        Fetch the current price for a given symbol.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :return: The current price
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.info(f"Fetched current price for {symbol}: {price}")
            return price
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching current price for {symbol}: {e}")
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_order_book(self, symbol, limit=100):
        """
        Fetch the order book for a given symbol.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param limit: The number of order book entries to fetch
        :return: The order book data
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            order_book = self.client.get_order_book(symbol=symbol, limit=limit)
            logger.info(f"Fetched order book for {symbol} with limit {limit}")
            return order_book
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching order book for {symbol}: {e}")
            raise e

# Example usage:
# api_key = 'your_api_key'
# api_secret = 'your_api_secret'
# fetcher = DataFetcher(api_key, api_secret)
# print(fetcher.get_historical_data('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan, 2021'))
# print(fetcher.get_current_price('BTCUSDT'))
# print(fetcher.get_order_book('BTCUSDT'))
