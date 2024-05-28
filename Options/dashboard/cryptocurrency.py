
import requests

class Cryptocurrency:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.binance.com'

    def get_price(self, symbol):
        endpoint = f'/api/v3/ticker/price?symbol={symbol}'
        response = requests.get(self.base_url + endpoint)
        return response.json()

    def get_historical_data(self, symbol, start_time, end_time):
        endpoint = f'/api/v3/klines?symbol={symbol}&interval=1d&startTime={start_time}&endTime={end_time}'
        response = requests.get(self.base_url + endpoint)
        return response.json()
