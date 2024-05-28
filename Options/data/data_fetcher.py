from binance.client import Client

class DataFetcher:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_historical_data(self, symbol, interval, start_str, end_str=None):
        """
        Fetches historical market data for a given symbol and interval.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param interval: The interval for candlesticks, e.g., Client.KLINE_INTERVAL_1HOUR
        :param start_str: The start date string in '1 Dec, 2021' format
        :param end_str: The end date string in '1 Jan, 2022' format (optional)
        :return: A list of candlestick data
        """
        return self.client.get_historical_klines(symbol, interval, start_str, end_str)

    def get_current_price(self, symbol):
        """
        Fetches the current price for a given symbol.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :return: The current price
        """
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

    def get_order_book(self, symbol, limit=100):
        """
        Fetches the order book for a given symbol.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param limit: The number of order book entries to fetch
        :return: The order book data
        """
        return self.client.get_order_book(symbol=symbol, limit=limit)

# Example usage:
# api_key = 'your_api_key'
# api_secret = 'your_api_secret'
# fetcher = DataFetcher(api_key, api_secret)
# print(fetcher.get_historical_data('BTCUSDT', Client.KLINE_INTERVAL_1DAY, '1 Jan, 2021'))
# print(fetcher.get_current_price('BTCUSDT'))
# print(fetcher.get_order_book('BTCUSDT'))
