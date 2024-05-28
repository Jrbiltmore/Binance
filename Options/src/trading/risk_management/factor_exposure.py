import pandas as pd
import numpy as np
import logging
from sklearn.linear_model import LinearRegression

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FactorExposure:
    def __init__(self, factor_returns, portfolio_returns):
        """
        Initialize the FactorExposure with factor and portfolio returns.

        :param factor_returns: DataFrame containing factor returns with factors as columns
        :param portfolio_returns: Series of portfolio returns
        """
        self.factor_returns = factor_returns
        self.portfolio_returns = portfolio_returns
        self.exposures = self.calculate_exposures()
        logger.info("FactorExposure initialized with factor and portfolio returns")

    def calculate_exposures(self):
        """
        Calculate the factor exposures of the portfolio.

        :return: DataFrame containing factor exposures
        """
        model = LinearRegression()
        model.fit(self.factor_returns, self.portfolio_returns)
        exposures = pd.Series(model.coef_, index=self.factor_returns.columns)
        logger.info(f"Calculated factor exposures:\n{exposures}")
        return exposures

    def calculate_portfolio_variance(self):
        """
        Calculate the variance of the portfolio due to factor exposures.

        :return: Portfolio variance
        """
        factor_cov_matrix = self.factor_returns.cov()
        portfolio_variance = np.dot(self.exposures.T, np.dot(factor_cov_matrix, self.exposures))
        logger.info(f"Calculated portfolio variance due to factor exposures: {portfolio_variance}")
        return portfolio_variance

    def calculate_marginal_contributions(self):
        """
        Calculate the marginal contribution of each factor to portfolio risk.

        :return: Series containing marginal contributions to portfolio risk
        """
        factor_cov_matrix = self.factor_returns.cov()
        marginal_contributions = np.dot(factor_cov_matrix, self.exposures)
        logger.info(f"Calculated marginal contributions to portfolio risk:\n{marginal_contributions}")
        return pd.Series(marginal_contributions, index=self.factor_returns.columns)

    def calculate_percentage_contributions(self):
        """
        Calculate the percentage contribution of each factor to portfolio risk.

        :return: Series containing percentage contributions to portfolio risk
        """
        marginal_contributions = self.calculate_marginal_contributions()
        portfolio_variance = self.calculate_portfolio_variance()
        percentage_contributions = marginal_contributions * self.exposures / portfolio_variance
        logger.info(f"Calculated percentage contributions to portfolio risk:\n{percentage_contributions}")
        return pd.Series(percentage_contributions, index=self.factor_returns.columns)

# Example usage:
if __name__ == "__main__":
    # Example factor returns data
    factor_data = {
        'Factor_A': np.random.normal(0, 0.01, 1000),
        'Factor_B': np.random.normal(0, 0.02, 1000),
        'Factor_C': np.random.normal(0, 0.015, 1000)
    }
    factor_returns = pd.DataFrame(factor_data)

    # Example portfolio returns
    portfolio_returns = pd.Series(np.random.normal(0, 0.01, 1000))

    factor_exposure = FactorExposure(factor_returns, portfolio_returns)
    
    exposures = factor_exposure.calculate_exposures()
    print(f"Factor exposures:\n{exposures}")

    portfolio_variance = factor_exposure.calculate_portfolio_variance()
    print(f"Portfolio variance due to factor exposures: {portfolio_variance}")

    marginal_contributions = factor_exposure.calculate_marginal_contributions()
    print(f"Marginal contributions to portfolio risk:\n{marginal_contributions}")

    percentage_contributions = factor_exposure.calculate_percentage_contributions()
    print(f"Percentage contributions to portfolio risk:\n{percentage_contributions}")
