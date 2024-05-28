import numpy as np
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicHedging:
    def __init__(self, portfolio_returns, benchmark_returns, delta_hedging=True):
        """
        Initialize the DynamicHedging with portfolio and benchmark returns.

        :param portfolio_returns: Series of portfolio returns
        :param benchmark_returns: Series of benchmark returns
        :param delta_hedging: Boolean indicating whether to use delta hedging
        """
        self.portfolio_returns = portfolio_returns
        self.benchmark_returns = benchmark_returns
        self.delta_hedging = delta_hedging
        self.beta = self.calculate_beta()
        logger.info(f"DynamicHedging initialized with beta: {self.beta}")

    def calculate_beta(self):
        """
        Calculate the beta of the portfolio relative to the benchmark.

        :return: Beta value
        """
        covariance_matrix = np.cov(self.portfolio_returns, self.benchmark_returns)
        beta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        logger.info(f"Calculated beta: {beta}")
        return beta

    def calculate_hedge_ratio(self):
        """
        Calculate the hedge ratio based on beta or delta.

        :return: Hedge ratio
        """
        if self.delta_hedging:
            hedge_ratio = -self.beta
        else:
            hedge_ratio = 1 / self.beta
        logger.info(f"Calculated hedge ratio: {hedge_ratio}")
        return hedge_ratio

    def apply_dynamic_hedging(self, portfolio_value, benchmark_value):
        """
        Apply dynamic hedging to the portfolio.

        :param portfolio_value: Value of the portfolio
        :param benchmark_value: Value of the benchmark
        :return: Number of benchmark units to trade for hedging
        """
        hedge_ratio = self.calculate_hedge_ratio()
        hedge_units = hedge_ratio * (portfolio_value / benchmark_value)
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

    dynamic_hedger = DynamicHedging(portfolio_returns, benchmark_returns)
    hedge_units = dynamic_hedger.apply_dynamic_hedging(portfolio_value, benchmark_value)
    print(f"Number of benchmark units to trade for hedging: {hedge_units}")
