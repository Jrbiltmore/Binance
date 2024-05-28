import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, data):
        """
        Initialize the DataProcessor with data.
        
        :param data: DataFrame containing market data
        """
        self.data = data

    def calculate_moving_average(self, window):
        """
        Calculate the moving average of the closing prices.
        
        :param window: The window size for the moving average
        :return: DataFrame with moving average
        """
        self.data[f'SMA_{window}'] = self.data['close'].rolling(window=window).mean()
        return self.data

    def calculate_exponential_moving_average(self, span):
        """
        Calculate the exponential moving average of the closing prices.
        
        :param span: The span for the exponential moving average
        :return: DataFrame with exponential moving average
        """
        self.data[f'EMA_{span}'] = self.data['close'].ewm(span=span, adjust=False).mean()
        return self.data

    def calculate_volatility(self, window):
        """
        Calculate the volatility of the closing prices.
        
        :param window: The window size for the rolling standard deviation
        :return: DataFrame with volatility
        """
        self.data[f'Volatility_{window}'] = self.data['close'].rolling(window=window).std()
        return self.data

    def calculate_relative_strength_index(self, window):
        """
        Calculate the Relative Strength Index (RSI).
        
        :param window: The window size for RSI calculation
        :return: DataFrame with RSI
        """
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        self.data[f'RSI_{window}'] = 100 - (100 / (1 + rs))
        return self.data

# Example usage:
# data = pd.DataFrame({
#     'close': [100, 102, 101, 105, 110, 107, 115, 120]
# })
# processor = DataProcessor(data)
# print(processor.calculate_moving_average(3))
# print(processor.calculate_exponential_moving_average(3))
# print(processor.calculate_volatility(3))
# print(processor.calculate_relative_strength_index(3))
