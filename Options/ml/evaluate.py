import pandas as pd
import numpy as np
import logging
from metrics import Metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrategyEvaluator:
    def __init__(self, returns, benchmark_returns=None, risk_free_rate=0.0):
        """
        Initialize the StrategyEvaluator with returns and optional benchmark returns.
        
        :param returns: Series of portfolio returns
        :param benchmark_returns: Series of benchmark returns (optional)
        :param risk_free_rate: Risk-free rate, default is 0.0
        """
        self.returns = returns
        self.benchmark_returns = benchmark_returns
        self.risk_free_rate = risk_free_rate
        logger.info("StrategyEvaluator initialized")

    def calculate_sharpe_ratio(self):
        """
        Calculate the Sharpe Ratio of the returns.

        :return: Sharpe Ratio
        """
        try:
            sharpe_ratio = Metrics.calculate_sharpe_ratio(self.returns, self.risk_free_rate)
            logger.info(f"Sharpe Ratio calculated: {sharpe_ratio}")
            return sharpe_ratio
        except ValueError as e:
            logger.error(f"Error calculating Sharpe Ratio: {e}")
            return None

    def calculate_max_drawdown(self):
        """
        Calculate the maximum drawdown of the returns.

        :return: Maximum drawdown
        """
        try:
            max_drawdown = Metrics.calculate_max_drawdown(self.returns)
            logger.info(f"Max Drawdown calculated: {max_drawdown}")
            return max_drawdown
        except ValueError as e:
            logger.error(f"Error calculating Max Drawdown: {e}")
            return None

    def calculate_sortino_ratio(self):
        """
        Calculate the Sortino Ratio of the returns.

        :return: Sortino Ratio
        """
        try:
            sortino_ratio = Metrics.calculate_sortino_ratio(self.returns, self.risk_free_rate)
            logger.info(f"Sortino Ratio calculated: {sortino_ratio}")
            return sortino_ratio
        except ValueError as e:
            logger.error(f"Error calculating Sortino Ratio: {e}")
            return None

    def calculate_alpha(self):
        """
        Calculate the alpha of the portfolio.

        :return: Alpha
        """
        if self.benchmark_returns is None:
            logger.error("Benchmark returns are required to calculate alpha")
            return None
        try:
            beta = Metrics.calculate_beta(self.returns, self.benchmark_returns)
            portfolio_return = np.mean(self.returns)
            benchmark_return = np.mean(self.benchmark_returns)
            alpha = Metrics.calculate_alpha(beta, portfolio_return, benchmark_return, self.risk_free_rate)
            logger.info(f"Alpha calculated: {alpha}")
            return alpha
        except ValueError as e:
            logger.error(f"Error calculating Alpha: {e}")
            return None

    def calculate_beta(self):
        """
        Calculate the beta of the portfolio.

        :return: Beta
        """
        if self.benchmark_returns is None:
            logger.error("Benchmark returns are required to calculate beta")
            return None
        try:
            beta = Metrics.calculate_beta(self.returns, self.benchmark_returns)
            logger.info(f"Beta calculated: {beta}")
            return beta
        except ValueError as e:
            logger.error(f"Error calculating Beta: {e}")
            return None

    def calculate_information_ratio(self):
        """
        Calculate the Information Ratio of the portfolio.

        :return: Information Ratio
        """
        if self.benchmark_returns is None:
            logger.error("Benchmark returns are required to calculate Information Ratio")
            return None
        try:
            information_ratio = Metrics.calculate_information_ratio(self.returns, self.benchmark_returns)
            logger.info(f"Information Ratio calculated: {information_ratio}")
            return information_ratio
        except ValueError as e:
            logger.error(f"Error calculating Information Ratio: {e}")
            return None

    def calculate_calmar_ratio(self):
        """
        Calculate the Calmar Ratio of the returns.

        :return: Calmar Ratio
        """
        try:
            calmar_ratio = Metrics.calculate_calmar_ratio(self.returns)
            logger.info(f"Calmar Ratio calculated: {calmar_ratio}")
            return calmar_ratio
        except ValueError as e:
            logger.error(f"Error calculating Calmar Ratio: {e}")
            return None

    def calculate_treynor_ratio(self):
        """
        Calculate the Treynor Ratio of the returns.

        :return: Treynor Ratio
        """
        if self.benchmark_returns is None:
            logger.error("Benchmark returns are required to calculate Treynor Ratio")
            return None
        try:
            treynor_ratio = Metrics.calculate_treynor_ratio(self.returns, self.benchmark_returns, self.risk_free_rate)
            logger.info(f"Treynor Ratio calculated: {treynor_ratio}")
            return treynor_ratio
        except ValueError as e:
            logger.error(f"Error calculating Treynor Ratio: {e}")
            return None

    def calculate_volatility(self):
        """
        Calculate the volatility of the returns.

        :return: Volatility
        """
        try:
            volatility = Metrics.calculate_volatility(self.returns)
            logger.info(f"Volatility calculated: {volatility}")
            return volatility
        except ValueError as e:
            logger.error(f"Error calculating Volatility: {e}")
            return None

# Example usage:
# returns = pd.Series([0.01, 0.02, 0.015, -0.005, 0.02])
# benchmark_returns = pd.Series([0.01, 0.015, 0.01, -0.01, 0.015])
# evaluator = StrategyEvaluator(returns, benchmark_returns)
# print("Sharpe Ratio:", evaluator.calculate_sharpe_ratio())
# print("Max Drawdown:", evaluator.calculate_max_drawdown())
# print("Sortino Ratio:", evaluator.calculate_sortino_ratio())
# print("Alpha:", evaluator.calculate_alpha())
# print("Beta:", evaluator.calculate_beta())
# print("Information Ratio:", evaluator.calculate_information_ratio())
# print("Calmar Ratio:", evaluator.calculate_calmar_ratio())
# print("Treynor Ratio:", evaluator.calculate_treynor_ratio())
# print("Volatility:", evaluator.calculate_volatility())
