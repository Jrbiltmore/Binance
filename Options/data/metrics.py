import pandas as pd
import numpy as np

class Metrics:
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
        """
        Calculate the Sharpe Ratio.

        :param returns: Series of returns
        :param risk_free_rate: Risk-free rate, default is 0.0
        :return: Sharpe Ratio
        :raises ValueError: If returns series is empty or standard deviation is zero
        """
        if returns.empty:
            raise ValueError("Returns series is empty.")
        excess_returns = returns - risk_free_rate
        std_dev = np.std(excess_returns)
        if std_dev == 0:
            raise ValueError("Standard deviation of returns is zero.")
        return np.mean(excess_returns) / std_dev

    @staticmethod
    def calculate_max_drawdown(returns):
        """
        Calculate the maximum drawdown.

        :param returns: Series of returns
        :return: Maximum drawdown
        :raises ValueError: If returns series is empty
        """
        if returns.empty:
            raise ValueError("Returns series is empty.")
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        return drawdown.min()

    @staticmethod
    def calculate_sortino_ratio(returns, risk_free_rate=0.0):
        """
        Calculate the Sortino Ratio.

        :param returns: Series of returns
        :param risk_free_rate: Risk-free rate, default is 0.0
        :return: Sortino Ratio
        :raises ValueError: If returns series is empty or downside deviation is zero
        """
        if returns.empty:
            raise ValueError("Returns series is empty.")
        downside_returns = returns[returns < risk_free_rate]
        downside_risk = np.std(downside_returns)
        if downside_risk == 0:
            raise ValueError("Downside risk is zero.")
        expected_return = np.mean(returns) - risk_free_rate
        return expected_return / downside_risk

    @staticmethod
    def calculate_alpha(beta, portfolio_return, benchmark_return, risk_free_rate=0.0):
        """
        Calculate the alpha of the portfolio.

        :param beta: Beta of the portfolio
        :param portfolio_return: Portfolio return
        :param benchmark_return: Benchmark return
        :param risk_free_rate: Risk-free rate, default is 0.0
        :return: Alpha
        """
        return portfolio_return - (risk_free_rate + beta * (benchmark_return - risk_free_rate))

    @staticmethod
    def calculate_beta(returns, benchmark_returns):
        """
        Calculate the beta of the portfolio.

        :param returns: Series of portfolio returns
        :param benchmark_returns: Series of benchmark returns
        :return: Beta
        :raises ValueError: If returns or benchmark_returns series is empty or benchmark variance is zero
        """
        if returns.empty or benchmark_returns.empty:
            raise ValueError("Returns or benchmark returns series is empty.")
        covariance = np.cov(returns, benchmark_returns)[0, 1]
        variance = np.var(benchmark_returns)
        if variance == 0:
            raise ValueError("Variance of benchmark returns is zero.")
        return covariance / variance

    @staticmethod
    def calculate_information_ratio(returns, benchmark_returns):
        """
        Calculate the Information Ratio.

        :param returns: Series of portfolio returns
        :param benchmark_returns: Series of benchmark returns
        :return: Information Ratio
        :raises ValueError: If returns or benchmark_returns series is empty or tracking error is zero
        """
        if returns.empty or benchmark_returns.empty:
            raise ValueError("Returns or benchmark returns series is empty.")
        active_return = returns - benchmark_returns
        tracking_error = np.std(active_return)
        if tracking_error == 0:
            raise ValueError("Tracking error is zero.")
        return np.mean(active_return) / tracking_error

    @staticmethod
    def calculate_calmar_ratio(returns):
        """
        Calculate the Calmar Ratio.

        :param returns: Series of returns
        :return: Calmar Ratio
        :raises ValueError: If returns series is empty or max drawdown is zero
        """
        if returns.empty:
            raise ValueError("Returns series is empty.")
        annual_return = np.mean(returns) * 252
        max_drawdown = Metrics.calculate_max_drawdown(returns)
        if max_drawdown == 0:
            raise ValueError("Maximum drawdown is zero.")
        return annual_return / abs(max_drawdown)

    @staticmethod
    def calculate_treynor_ratio(returns, benchmark_returns, risk_free_rate=0.0):
        """
        Calculate the Treynor Ratio.

        :param returns: Series of portfolio returns
        :param benchmark_returns: Series of benchmark returns
        :param risk_free_rate: Risk-free rate, default is 0.0
        :return: Treynor Ratio
        :raises ValueError: If returns or benchmark_returns series is empty or beta is zero
        """
        if returns.empty or benchmark_returns.empty:
            raise ValueError("Returns or benchmark returns series is empty.")
        beta = Metrics.calculate_beta(returns, benchmark_returns)
        if beta == 0:
            raise ValueError("Beta is zero.")
        excess_returns = returns - risk_free_rate
        return np.mean(excess_returns) / beta

    @staticmethod
    def calculate_volatility(returns):
        """
        Calculate the volatility of the returns.

        :param returns: Series of returns
        :return: Volatility
        :raises ValueError: If returns series is empty
        """
        if returns.empty:
            raise ValueError("Returns series is empty.")
        return np.std(returns)

# Example usage:
# returns = pd.Series([0.01, 0.02, 0.015, -0.005, 0.02])
# benchmark_returns = pd.Series([0.01, 0.015, 0.01, -0.01, 0.015])
# metrics = Metrics()
# print("Sharpe Ratio:", metrics.calculate_sharpe_ratio(returns))
# print("Max Drawdown:", metrics.calculate_max_drawdown(returns))
# print("Sortino Ratio:", metrics.calculate_sortino_ratio(returns))
# print("Alpha:", metrics.calculate_alpha(1.2, 0.02, 0.015))
# print("Beta:", metrics.calculate_beta(returns, benchmark_returns))
# print("Information Ratio:", metrics.calculate_information_ratio(returns, benchmark_returns))
# print("Calmar Ratio:", metrics.calculate_calmar_ratio(returns))
# print("Treynor Ratio:", metrics.calculate_treynor_ratio(returns, benchmark_returns))
# print("Volatility:", metrics.calculate_volatility(returns))
