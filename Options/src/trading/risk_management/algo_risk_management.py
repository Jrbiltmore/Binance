import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlgorithmicRiskManagement:
    def __init__(self, portfolio_value, risk_tolerance):
        """
        Initialize the AlgorithmicRiskManagement with portfolio value and risk tolerance.

        :param portfolio_value: Total value of the portfolio
        :param risk_tolerance: Maximum allowable risk per trade as a percentage of the portfolio value
        """
        self.portfolio_value = portfolio_value
        self.risk_tolerance = risk_tolerance
        logger.info(f"AlgorithmicRiskManagement initialized with portfolio value: {portfolio_value} and risk tolerance: {risk_tolerance}%")

    def calculate_position_size(self, stop_loss_amount):
        """
        Calculate the position size based on risk tolerance and stop loss amount.

        :param stop_loss_amount: Amount risked per trade (difference between entry price and stop loss price)
        :return: Position size
        """
        risk_per_trade = self.portfolio_value * (self.risk_tolerance / 100)
        position_size = risk_per_trade / stop_loss_amount
        logger.info(f"Calculated position size: {position_size} for stop loss amount: {stop_loss_amount}")
        return position_size

    def calculate_max_drawdown(self, returns):
        """
        Calculate the maximum drawdown from a series of returns.

        :param returns: Series of returns
        :return: Maximum drawdown
        """
        cumulative_returns = (1 + returns).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        max_drawdown = drawdown.min()
        logger.info(f"Calculated max drawdown: {max_drawdown}")
        return max_drawdown

    def apply_risk_limits(self, trade_risk):
        """
        Apply risk limits to a proposed trade.

        :param trade_risk: Risk of the proposed trade as a percentage of the portfolio value
        :return: Boolean indicating whether the trade is within risk limits
        """
        if trade_risk > self.risk_tolerance:
            logger.warning(f"Trade risk {trade_risk}% exceeds risk tolerance {self.risk_tolerance}%")
            return False
        logger.info(f"Trade risk {trade_risk}% is within risk tolerance {self.risk_tolerance}%")
        return True

    def calculate_value_at_risk(self, returns, confidence_level=0.95):
        """
        Calculate the Value at Risk (VaR) for a given series of returns.

        :param returns: Series of returns
        :param confidence_level: Confidence level for VaR calculation
        :return: Value at Risk
        """
        if returns.empty:
            logger.warning("Returns series is empty, cannot calculate VaR")
            return None

        var = np.percentile(returns, (1 - confidence_level) * 100)
        portfolio_var = self.portfolio_value * var
        logger.info(f"Calculated Value at Risk (VaR) at {confidence_level*100}% confidence level: {portfolio_var}")
        return portfolio_var

    def calculate_conditional_value_at_risk(self, returns, confidence_level=0.95):
        """
        Calculate the Conditional Value at Risk (CVaR) for a given series of returns.

        :param returns: Series of returns
        :param confidence_level: Confidence level for CVaR calculation
        :return: Conditional Value at Risk
        """
        if returns.empty:
            logger.warning("Returns series is empty, cannot calculate CVaR")
            return None

        var = self.calculate_value_at_risk(returns, confidence_level)
        cvar = returns[returns <= var].mean()
        portfolio_cvar = self.portfolio_value * cvar
        logger.info(f"Calculated Conditional Value at Risk (CVaR) at {confidence_level*100}% confidence level: {portfolio_cvar}")
        return portfolio_cvar

# Example usage:
if __name__ == "__main__":
    portfolio_value = 1000000  # Example portfolio value
    risk_tolerance = 1  # Example risk tolerance as a percentage of the portfolio value

    risk_manager = AlgorithmicRiskManagement(portfolio_value, risk_tolerance)

    # Example returns series
    returns = pd.Series(np.random.normal(0, 0.01, 1000))

    stop_loss_amount = 0.05  # Example stop loss amount
    position_size = risk_manager.calculate_position_size(stop_loss_amount)
    print(f"Position size: {position_size}")

    max_drawdown = risk_manager.calculate_max_drawdown(returns)
    print(f"Max drawdown: {max_drawdown}")

    trade_risk = 0.5  # Example trade risk as a percentage of the portfolio value
    is_within_limits = risk_manager.apply_risk_limits(trade_risk)
    print(f"Is trade within risk limits: {is_within_limits}")

    var = risk_manager.calculate_value_at_risk(returns)
    print(f"Value at Risk (VaR): {var}")

    cvar = risk_manager.calculate_conditional_value_at_risk(returns)
    print(f"Conditional Value at Risk (CVaR): {cvar}")
