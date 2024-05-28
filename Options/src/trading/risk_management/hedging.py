import numpy as np
import pandas as pd
import logging
from scipy.stats import linregress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Hedging:
    def __init__(self, portfolio_returns, benchmark_returns):
        """
        Initialize the Hedging class with portfolio and benchmark returns.

        :param portfolio_returns: Series of portfolio returns
        :param benchmark_returns: Series of benchmark returns
        """
        self.portfolio_returns = portfolio_returns
        self.benchmark_returns = benchmark_returns
        self.hedge_ratio = self.calculate_hedge_ratio()
        logger.info(f"Hedging initialized with hedge ratio: {self.hedge_ratio}")

    def calculate_hedge_ratio(self):
        """
        Calculate the hedge ratio using linear regression.

        :return: Hedge ratio
        """
        slope, intercept, r_value, p_value, std_err = linregress(self.benchmark_returns, self.portfolio_returns)
        hedge_ratio = slope
        logger.info(f"Calculated hedge ratio: {hedge_ratio}")
        return hedge_ratio

    def apply_hedging(self, portfolio_value, benchmark_value):
        """
        Apply hedging to the portfolio.

        :param portfolio_value: Value of the portfolio
        :param benchmark_value: Value of the benchmark
        :return: Number of benchmark units to trade for hedging
        """
        hedge_units = self.hedge_ratio * (portfolio_value / benchmark_value)
        logger.info(f"Calculated hedge units: {hedge_units}")
        return hedge_units

# Example usage:
if __name__ == "__main__":
    # Example portfolio and benchmark returns
    portfolio_returns = pd.Series(np.random.normal(0.01, 0.02, 1000))
    benchmark_returns = pd.Series(np.random.normal(0.01, 0.02, 1000))

    # Example portfolio and benchmark values
    portfolio_value = 1000000  # Example portfolio value of 1,000,000
    benchmark_value = 2000  # Example benchmark value (e.g., price of SPY)

    hedging = Hedging(portfolio_returns, benchmark_returns)
    hedge_units = hedging.apply_hedging(portfolio_value, benchmark_value)
    print(f"Number of benchmark units to trade for hedging: {hedge_units}")
