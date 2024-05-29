import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValueAtRisk:
    def __init__(self, returns, confidence_level=0.95):
        """
        Initialize the ValueAtRisk with asset returns and confidence level.

        :param returns: DataFrame containing asset returns
        :param confidence_level: Confidence level for VaR calculation (default is 95%)
        """
        self.returns = returns
        self.confidence_level = confidence_level
        logger.info("ValueAtRisk initialized with returns and confidence level")

    def historical_var(self):
        """
        Calculate the historical VaR for the portfolio.

        :return: Historical VaR value
        """
        var_value = self.returns.quantile(1 - self.confidence_level)
        logger.info(f"Calculated historical VaR: {var_value}")
        return var_value

    def parametric_var(self):
        """
        Calculate the parametric VaR for the portfolio assuming normal distribution.

        :return: Parametric VaR value
        """
        mean = self.returns.mean()
        std_dev = self.returns.std()
        var_value = mean - std_dev * np.abs(np.percentile(self.returns, (1 - self.confidence_level) * 100))
        logger.info(f"Calculated parametric VaR: {var_value}")
        return var_value

    def monte_carlo_var(self, simulations=10000):
        """
        Calculate the Monte Carlo VaR for the portfolio.

        :param simulations: Number of simulations to run (default is 10000)
        :return: Monte Carlo VaR value
        """
        simulated_returns = np.random.choice(self.returns, (simulations, len(self.returns)))
        portfolio_returns = simulated_returns.sum(axis=1)
        var_value = np.percentile(portfolio_returns, (1 - self.confidence_level) * 100)
        logger.info(f"Calculated Monte Carlo VaR: {var_value}")
        return var_value

# Example usage:
if __name__ == "__main__":
    # Example returns data
    returns_data = {
        'Asset_A': np.random.normal(0.001, 0.02, 1000),
        'Asset_B': np.random.normal(0.0012, 0.022, 1000),
        'Asset_C': np.random.normal(0.0008, 0.018, 1000),
        'Asset_D': np.random.normal(0.0011, 0.019, 1000),
    }
    returns_df = pd.DataFrame(returns_data)

    var_calculator = ValueAtRisk(returns_df)
    
    historical_var_value = var_calculator.historical_var()
    print(f"Historical VaR: {historical_var_value}")

    parametric_var_value = var_calculator.parametric_var()
    print(f"Parametric VaR: {parametric_var_value}")

    monte_carlo_var_value = var_calculator.monte_carlo_var()
    print(f"Monte Carlo VaR: {monte_carlo_var_value}")
