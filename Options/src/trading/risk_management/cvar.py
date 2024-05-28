import numpy as np
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConditionalValueAtRisk:
    def __init__(self, returns, confidence_level=0.95):
        """
        Initialize the ConditionalValueAtRisk with returns and confidence level.

        :param returns: Series of portfolio returns
        :param confidence_level: Confidence level for CVaR calculation, default is 0.95
        """
        self.returns = returns
        self.confidence_level = confidence_level
        logger.info(f"ConditionalValueAtRisk initialized with confidence level: {confidence_level}")

    def calculate_var(self):
        """
        Calculate the Value at Risk (VaR) for the returns.

        :return: Value at Risk (VaR)
        """
        var = np.percentile(self.returns, (1 - self.confidence_level) * 100)
        logger.info(f"Calculated Value at Risk (VaR): {var}")
        return var

    def calculate_cvar(self):
        """
        Calculate the Conditional Value at Risk (CVaR) for the returns.

        :return: Conditional Value at Risk (CVaR)
        """
        var = self.calculate_var()
        cvar = self.returns[self.returns <= var].mean()
        logger.info(f"Calculated Conditional Value at Risk (CVaR): {cvar}")
        return cvar

# Example usage:
if __name__ == "__main__":
    # Example portfolio returns
    portfolio_returns = pd.Series(np.random.normal(-0.01, 0.02, 1000))

    cvar_calculator = ConditionalValueAtRisk(portfolio_returns)
    var = cvar_calculator.calculate_var()
    print(f"Value at Risk (VaR): {var}")

    cvar = cvar_calculator.calculate_cvar()
    print(f"Conditional Value at Risk (CVaR): {cvar}")
