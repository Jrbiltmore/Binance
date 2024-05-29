import pandas as pd
import numpy as np
import logging
from statsmodels.tsa.stattools import coint

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StatisticalArbitrage:
    def __init__(self, price_data):
        """
        Initialize the StatisticalArbitrage with price data.

        :param price_data: DataFrame containing price data with assets as columns
        """
        self.price_data = price_data
        logger.info("StatisticalArbitrage initialized with price data")

    def find_cointegrated_pairs(self):
        """
        Find all pairs of assets that are cointegrated.

        :return: List of tuples containing cointegrated pairs
        """
        n = self.price_data.shape[1]
        keys = self.price_data.columns
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                asset1 = self.price_data[keys[i]]
                asset2 = self.price_data[keys[j]]
                score, p_value, _ = coint(asset1, asset2)
                if p_value < 0.05:  # Using a significance level of 5%
                    pairs.append((keys[i], keys[j]))
                    logger.info(f"Cointegrated pair found: {keys[i]} and {keys[j]} with p-value: {p_value}")
        return pairs

    def calculate_spread(self, asset1, asset2):
        """
        Calculate the spread between two cointegrated assets.

        :param asset1: Series containing price data for the first asset
        :param asset2: Series containing price data for the second asset
        :return: Series containing the spread
        """
        spread = asset1 - asset2
        logger.info(f"Calculated spread between assets")
        return spread

    def calculate_z_score(self, spread):
        """
        Calculate the z-score of the spread.

        :param spread: Series containing the spread
        :return: Series containing the z-score
        """
        mean = spread.mean()
        std = spread.std()
        z_score = (spread - mean) / std
        logger.info(f"Calculated z-score for spread")
        return z_score

    def generate_trading_signals(self, z_score, entry_threshold=2.0, exit_threshold=0.5):
        """
        Generate trading signals based on z-score thresholds.

        :param z_score: Series containing the z-score
        :param entry_threshold: Z-score threshold for entering trades (default is 2.0)
        :param exit_threshold: Z-score threshold for exiting trades (default is 0.5)
        :return: Series containing trading signals
        """
        signals = pd.Series(index=z_score.index)
        signals[z_score > entry_threshold] = -1  # Short the spread
        signals[z_score < -entry_threshold] = 1  # Long the spread
        signals[(z_score < exit_threshold) & (z_score > -exit_threshold)] = 0  # Exit trades
        signals = signals.fillna(0)
        logger.info(f"Generated trading signals based on z-score thresholds")
        return signals

# Example usage:
if __name__ == "__main__":
    # Example price data
    price_data = {
        'Asset_A': np.random.normal(100, 1, 100),
        'Asset_B': np.random.normal(100, 1, 100),
        'Asset_C': np.random.normal(100, 1, 100),
        'Asset_D': np.random.normal(100, 1, 100)
    }
    price_df = pd.DataFrame(price_data)

    stat_arb = StatisticalArbitrage(price_df)

    # Find cointegrated pairs
    cointegrated_pairs = stat_arb.find_cointegrated_pairs()
    print(f"Cointegrated pairs: {cointegrated_pairs}")

    if cointegrated_pairs:
        asset1, asset2 = cointegrated_pairs[0]
        spread = stat_arb.calculate_spread(price_df[asset1], price_df[asset2])
        z_score = stat_arb.calculate_z_score(spread)
        trading_signals = stat_arb.generate_trading_signals(z_score)
        print(f"Trading signals for pair {asset1} and {asset2}:\n{trading_signals}")
