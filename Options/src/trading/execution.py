import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Execution:
    def __init__(self, api_client):
        """
        Initialize the Execution with an API client for trading operations.

        :param api_client: An API client instance for executing trades
        """
        self.api_client = api_client
        logger.info("Execution initialized with API client")

    def place_order(self, symbol, quantity, order_type='market', price=None):
        """
        Place an order in the market.

        :param symbol: Trading symbol (e.g., 'BTCUSDT')
        :param quantity: Quantity to trade
        :param order_type: Type of order ('market' or 'limit')
        :param price: Price for limit orders
        :return: Order response from the API
        """
        try:
            if order_type == 'market':
                order = self.api_client.order_market(symbol=symbol, quantity=quantity)
            elif order_type == 'limit':
                if price is None:
                    raise ValueError("Price must be specified for limit orders")
                order = self.api_client.order_limit(symbol=symbol, quantity=quantity, price=price)
            else:
                raise ValueError("Invalid order type")
            logger.info(f"Placed {order_type} order for {quantity} of {symbol} at {price if price else 'market price'}")
            return order
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            raise

    def cancel_order(self, symbol, order_id):
        """
        Cancel an existing order.

        :param symbol: Trading symbol (e.g., 'BTCUSDT')
        :param order_id: ID of the order to cancel
        :return: Cancel response from the API
        """
        try:
            cancel_response = self.api_client.cancel_order(symbol=symbol, order_id=order_id)
            logger.info(f"Canceled order {order_id} for {symbol}")
            return cancel_response
        except Exception as e:
            logger.error(f"Error canceling order: {e}")
            raise

    def get_order_status(self, symbol, order_id):
        """
        Get the status of an existing order.

        :param symbol: Trading symbol (e.g., 'BTCUSDT')
        :param order_id: ID of the order
        :return: Order status response from the API
        """
        try:
            order_status = self.api_client.get_order(symbol=symbol, order_id=order_id)
            logger.info(f"Order status for {order_id} of {symbol}: {order_status}")
            return order_status
        except Exception as e:
            logger.error(f"Error getting order status: {e}")
            raise

    def get_open_orders(self, symbol):
        """
        Get all open orders for a given symbol.

        :param symbol: Trading symbol (e.g., 'BTCUSDT')
        :return: List of open orders from the API
        """
        try:
            open_orders = self.api_client.get_open_orders(symbol=symbol)
            logger.info(f"Retrieved open orders for {symbol}: {open_orders}")
            return open_orders
        except Exception as e:
            logger.error(f"Error getting open orders: {e}")
            raise

    def get_trade_history(self, symbol):
        """
        Get the trade history for a given symbol.

        :param symbol: Trading symbol (e.g., 'BTCUSDT')
        :return: List of trade history from the API
        """
        try:
            trade_history = self.api_client.get_my_trades(symbol=symbol)
            logger.info(f"Retrieved trade history for {symbol}: {trade_history}")
            return trade_history
        except Exception as e:
            logger.error(f"Error getting trade history: {e}")
            raise

# Example usage:
if __name__ == "__main__":
    # Mock API client for example
    class MockAPIClient:
        def order_market(self, symbol, quantity):
            return {"symbol": symbol, "quantity": quantity, "type": "market", "status": "filled"}

        def order_limit(self, symbol, quantity, price):
            return {"symbol": symbol, "quantity": quantity, "type": "limit", "price": price, "status": "open"}

        def cancel_order(self, symbol, order_id):
            return {"symbol": symbol, "order_id": order_id, "status": "canceled"}

        def get_order(self, symbol, order_id):
            return {"symbol": symbol, "order_id": order_id, "status": "filled"}

        def get_open_orders(self, symbol):
            return [{"symbol": symbol, "order_id": 1, "status": "open"}]

        def get_my_trades(self, symbol):
            return [{"symbol": symbol, "order_id": 1, "quantity": 1, "price": 10000, "status": "filled"}]

    api_client = MockAPIClient()
    execution = Execution(api_client)

    # Place a market order
    execution.place_order(symbol='BTCUSDT', quantity=1)

    # Place a limit order
    execution.place_order(symbol='BTCUSDT', quantity=1, order_type='limit', price=9500)

    # Cancel an order
    execution.cancel_order(symbol='BTCUSDT', order_id=1)

    # Get order status
    execution.get_order_status(symbol='BTCUSDT', order_id=1)

    # Get open orders
    execution.get_open_orders(symbol='BTCUSDT')

    # Get trade history
    execution.get_trade_history(symbol='BTCUSDT')
