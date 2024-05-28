from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptionsExecution:
    def __init__(self, api_key, api_secret):
        """
        Initialize the OptionsExecution with Binance API credentials.

        :param api_key: Binance API key
        :param api_secret: Binance API secret
        """
        self.client = Client(api_key, api_secret)
        logger.info("Binance client initialized for options execution")

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place an order on the options market.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param side: 'BUY' or 'SELL'
        :param order_type: Type of order, e.g., 'LIMIT', 'MARKET'
        :param quantity: Quantity of the order
        :param price: Price of the order (required for LIMIT orders)
        :return: The order result
        :raises BinanceAPIException: If the Binance API returns an error
        :raises BinanceOrderException: If there is an issue with the order
        """
        try:
            if order_type == 'LIMIT':
                if price is None:
                    raise ValueError("Price must be specified for LIMIT orders")
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    timeInForce='GTC',
                    quantity=quantity,
                    price=price
                )
            elif order_type == 'MARKET':
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity
                )
            else:
                raise ValueError(f"Unsupported order type: {order_type}")

            logger.info(f"Placed {side} order for {quantity} of {symbol} at {price}")
            return order
        except (BinanceAPIException, BinanceOrderException, ValueError) as e:
            logger.error(f"Error placing {side} order for {symbol}: {e}")
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def query_order_status(self, symbol, order_id):
        """
        Query the status of an order.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param order_id: The ID of the order to query
        :return: The order status
        :raises BinanceAPIException: If the Binance API returns an error
        """
        try:
            order_status = self.client.get_order(symbol=symbol, orderId=order_id)
            logger.info(f"Queried order status for {order_id} of {symbol}: {order_status['status']}")
            return order_status
        except BinanceAPIException as e:
            logger.error(f"Error querying order status for {order_id} of {symbol}: {e}")
            raise e

    @retry(stop_max_attempt_number=5, wait_fixed=2000)
    def cancel_order(self, symbol, order_id):
        """
        Cancel an existing order.

        :param symbol: The trading symbol, e.g., 'BTCUSDT'
        :param order_id: The ID of the order to cancel
        :return: The result of the cancel request
        :raises BinanceAPIException: If the Binance API returns an error
        """
        try:
            cancel_result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"Canceled order {order_id} of {symbol}")
            return cancel_result
        except BinanceAPIException as e:
            logger.error(f"Error canceling order {order_id} of {symbol}: {e}")
            raise e

# Example usage:
# api_key = 'your_api_key'
# api_secret = 'your_api_secret'
# executor = OptionsExecution(api_key, api_secret)
# print(executor.place_order('BTCUSDT', 'BUY', 'LIMIT', 1, 40000))
# print(executor.query_order_status('BTCUSDT', 'order_id'))
# print(executor.cancel_order('BTCUSDT', 'order_id'))
