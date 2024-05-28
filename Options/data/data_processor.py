import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data):
        """
        Initialize the DataProcessor with data.
        
        :param data: DataFrame containing market data with a 'close' column
        """
        if 'close' not in data.columns:
            raise ValueError("DataFrame must contain a 'close' column")
        self.data = data
        logger.info("DataProcessor initialized with data")

    def calculate_moving_average(self, window):
        """
        Calculate the moving average of the closing prices.
        
        :param window: The window size for the moving average
        :return: DataFrame with moving average
        :raises ValueError: If window size is not positive
        """
        if window <= 0:
            raise ValueError("Window size must be positive")
        self.data[f'SMA_{window}'] = self.data['close'].rolling(window=window).mean()
        logger.info(f"Calculated {window}-day simple moving average")
        return self.data

    def calculate_exponential_moving_average(self, span):
        """
        Calculate the exponential moving average of the closing prices.
        
        :param span: The span for the exponential moving average
        :return: DataFrame with exponential moving average
        :raises ValueError: If span is not positive
        """
        if span <= 0:
            raise ValueError("Span must be positive")
        self.data[f'EMA_{span}'] = self.data['close'].ewm(span=span, adjust=False).mean()
        logger.info(f"Calculated {span}-day exponential moving average")
        return self.data

    def calculate_volatility(self, window):
        """
        Calculate the volatility of the closing prices.
        
        :param window: The window size for the rolling standard deviation
        :return: DataFrame with volatility
        :raises ValueError: If window size is not positive
        """
        if window <= 0:
            raise ValueError("Window size must be positive")
        self.data[f'Volatility_{window}'] = self.data['close'].rolling(window=window).std()
        logger.info(f"Calculated {window}-day volatility")
        return self.data

    def calculate_relative_strength_index(self, window):
        """
        Calculate the Relative Strength Index (RSI).
        
        :param window: The window size for RSI calculation
        :return: DataFrame with RSI
        :raises ValueError: If window size is not positive
        """
        if window <= 0:
            raise ValueError("Window size must be positive")
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        self.data[f'RSI_{window}'] = 100 - (100 / (1 + rs))
        logger.info(f"Calculated {window}-day Relative Strength Index (RSI)")
        return self.data

    def calculate_bollinger_bands(self, window, num_of_std):
        """
        Calculate Bollinger Bands.

        :param window: The window size for the moving average
        :param num_of_std: The number of standard deviations for the bands
        :return: DataFrame with Bollinger Bands
        :raises ValueError: If window size or number of standard deviations is not positive
        """
        if window <= 0 or num_of_std <= 0:
            raise ValueError("Window size and number of standard deviations must be positive")
        rolling_mean = self.data['close'].rolling(window=window).mean()
        rolling_std = self.data['close'].rolling(window=window).std()
        self.data['Bollinger_High'] = rolling_mean + (rolling_std * num_of_std)
        self.data['Bollinger_Low'] = rolling_mean - (rolling_std * num_of_std)
        logger.info(f"Calculated Bollinger Bands with {window}-day window and {num_of_std} standard deviations")
        return self.data

    def calculate_moving_average_convergence_divergence(self, fast_span, slow_span, signal_span):
        """
        Calculate the Moving Average Convergence Divergence (MACD).

        :param fast_span: The span for the fast exponential moving average
        :param slow_span: The span for the slow exponential moving average
        :param signal_span: The span for the signal line
        :return: DataFrame with MACD and signal line
        :raises ValueError: If any span is not positive
        """
        if fast_span <= 0 or slow_span <= 0 or signal_span <= 0:
            raise ValueError("All spans must be positive")
        fast_ema = self.data['close'].ewm(span=fast_span, adjust=False).mean()
        slow_ema = self.data['close'].ewm(span=slow_span, adjust=False).mean()
        self.data['MACD'] = fast_ema - slow_ema
        self.data['MACD_Signal'] = self.data['MACD'].ewm(span=signal_span, adjust=False).mean()
        logger.info(f"Calculated MACD with fast span {fast_span}, slow span {slow_span}, and signal span {signal_span}")
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
# print(processor.calculate_bollinger_bands(3, 2))
# print(processor.calculate_moving_average_convergence_divergence(12, 26, 9))
