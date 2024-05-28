import requests
import logging
from typing import Dict, Any

class BinanceAPI:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.binance.com"
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key
        })
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _create_signature(self, params: Dict[str, Any]) -> str:
        import hmac
        import hashlib
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, json=params)
            else:
                raise ValueError("Unsupported HTTP method")
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise
        except requests.Timeout as timeout_err:
            self.logger.error(f"Request timed out: {timeout_err}")
            raise
        except requests.TooManyRedirects as redirect_err:
            self.logger.error(f"Too many redirects: {redirect_err}")
            raise
        except Exception as err:
            self.logger.error(f"An error occurred: {err}")
            raise

    def get_account_info(self) -> Dict[str, Any]:
        endpoint = "/api/v3/account"
        params = {
            "timestamp": int(time.time() * 1000)
        }
        params['signature'] = self._create_signature(params)
        self.logger.debug(f"Fetching account info...")
        data = self._make_request('GET', endpoint, params)
        self.logger.debug(f"Account info: {data}")
        return data

    def get_symbol_price(self, symbol: str) -> Dict[str, Any]:
        endpoint = "/api/v3/ticker/price"
        params = {"symbol": symbol}
        self.logger.debug(f"Fetching price for symbol: {symbol}")
        data = self._make_request('GET', endpoint, params)
        self.logger.debug(f"Price data: {data}")
        return data

    def place_order(self, symbol: str, side: str, type: str, quantity: float, price: float = None, time_in_force: str = "GTC") -> Dict[str, Any]:
        endpoint = "/api/v3/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        if price:
            params["price"] = price
        if time_in_force:
            params["timeInForce"] = time_in_force
        params['signature'] = self._create_signature(params)
        self.logger.debug(f"Placing order: {params}")
        data = self._make_request('POST', endpoint, params)
        self.logger.debug(f"Order response: {data}")
        return data

    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        endpoint = "/api/v3/order"
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": int(time.time() * 1000)
        }
        params['signature'] = self._create_signature(params)
        self.logger.debug(f"Cancelling order: {params}")
        data = self._make_request('DELETE', endpoint, params)
        self.logger.debug(f"Cancel response: {data}")
        return data

    def get_open_orders(self, symbol: str = None) -> Dict[str, Any]:
        endpoint = "/api/v3/openOrders"
        params = {
            "timestamp": int(time.time() * 1000)
        }
        if symbol:
            params["symbol"] = symbol
        params['signature'] = self._create_signature(params)
        self.logger.debug(f"Fetching open orders...")
        data = self._make_request('GET', endpoint, params)
        self.logger.debug(f"Open orders: {data}")
        return data

    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        endpoint = "/api/v3/order"
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": int(time.time() * 1000)
        }
        params['signature'] = self._create_signature(params)
        self.logger.debug(f"Fetching order status for order_id: {order_id}")
        data = self._make_request('GET', endpoint, params)
        self.logger.debug(f"Order status: {data}")
        return data
