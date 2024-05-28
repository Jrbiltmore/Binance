from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import logging
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptionsDataFetcher:
    def __init__(self, api_key, api_secret):
        """
        Initialize the OptionsDataFetcher with Binance API credentials.

        :param api_key: Binance API key
        :param api_secret: Binance API secret
        """
        self.client = Client(api_key, api_secret)
        logger.info("Binance client initialized for options data fetching")

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_options_info(self):
        """
        Fetch information about available options trading pairs.

        :return: List of options trading pairs
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            options_info = self.client.options_info()
            logger.info("Fetched options trading pairs information")
            return options_info
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching options info: {e}")
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_options_prices(self, symbol):
        """
        Fetch the current prices for a given options trading pair.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :return: Current options prices
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            options_prices = self.client.options_prices(symbol=symbol)
            logger.info(f"Fetched current options prices for {symbol}")
            return options_prices
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching options prices for {symbol}: {e}")
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_options_order_book(self, symbol, limit=100):
        """
        Fetch the order book for a given options trading pair.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param limit: The number of order book entries to fetch
        :return: The options order book data
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            order_book = self.client.options_order_book(symbol=symbol, limit=limit)
            logger.info(f"Fetched options order book for {symbol} with limit {limit}")
            return order_book
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching options order book for {symbol}: {e}")
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def get_options_historical_data(self, symbol, interval, start_str, end_str=None):
        """
        Fetch historical options data for a given symbol and interval.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param interval: The interval for candlesticks, e.g., Client.KLINE_INTERVAL_1HOUR
        :param start_str: The start date string in '1 Dec, 2021' format
        :param end_str: The end date string in '1 Jan, 2022' format (optional)
        :return: A list of candlestick data
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceRequestException: If the request to Binance fails
        """
        try:
            historical_data = self.client.get_historical_klines(symbol, interval, start_str, end_str)
            logger.info(f"Fetched historical options data for {symbol} from {start_str} to {end_str}")
            return historical_data
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Error fetching historical options data for {symbol}: {e}")
            raise e

# Example usage:
# api_key = 'your_api_key'
# api_secret = 'your_api_secret'
# fetcher = OptionsDataFetcher(api_key, api_secret)
# print(fetcher.get_options_info())
# print(fetcher.get_options_prices('BTCUSDT'))
# print(fetcher.get_options_order_book('BTCUSDT'))
# print(fetcher.get_options_historical_data('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan, 2021'))
