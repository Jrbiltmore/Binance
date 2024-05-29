import numpy as np
import pandas as pd
import logging
from scipy.optimize import minimize

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SharpeRatioOptimization:
    def __init__(self, returns, risk_free_rate=0.01):
        """
        Initialize the SharpeRatioOptimization with asset returns and the risk-free rate.

        :param returns: DataFrame containing asset returns with assets as columns
        :param risk_free_rate: Risk-free rate for Sharpe ratio calculation (default is 1%)
        """
        self.returns = returns
        self.risk_free_rate = risk_free_rate
        logger.info("SharpeRatioOptimization initialized with returns and risk-free rate")

    def calculate_sharpe_ratio(self, weights):
        """
        Calculate the Sharpe ratio for a given set of portfolio weights.

        :param weights: Array of portfolio weights
        :return: Sharpe ratio
        """
        portfolio_return = np.sum(self.returns.mean() * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov() * 252, weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        logger.info(f"Calculated Sharpe ratio: {sharpe_ratio} for weights: {weights}")
        return sharpe_ratio

    def negative_sharpe_ratio(self, weights):
        """
        Calculate the negative Sharpe ratio for optimization (since we minimize).

        :param weights: Array of portfolio weights
        :return: Negative Sharpe ratio
        """
        return -self.calculate_sharpe_ratio(weights)

    def optimize_portfolio(self):
        """
        Optimize the portfolio to maximize the Sharpe ratio.

        :return: Optimal portfolio weights
        """
        num_assets = len(self.returns.columns)
        args = ()
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for asset in range(num_assets))
        initial_weights = num_assets * [1. / num_assets,]
        
        result = minimize(self.negative_sharpe_ratio, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimized_weights = result.x
            logger.info(f"Optimized portfolio weights: {optimized_weights}")
            return optimized_weights
        else:
            logger.error("Optimization failed")
            raise ValueError("Optimization failed")

    def get_optimized_portfolio(self):
        """
        Get the optimized portfolio details including weights, return, volatility, and Sharpe ratio.

        :return: Dictionary containing optimized portfolio details
        """
        optimized_weights = self.optimize_portfolio()
        portfolio_return = np.sum(self.returns.mean() * optimized_weights) * 252
        portfolio_volatility = np.sqrt(np.dot(optimized_weights.T, np.dot(self.returns.cov() * 252, optimized_weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        portfolio_details = {
            'weights': optimized_weights,
            'return': portfolio_return,
            'volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio
        }
        
        logger.info(f"Optimized portfolio details: {portfolio_details}")
        return portfolio_details

# Example usage:
if __name__ == "__main__":
    # Example asset returns data
    returns_data = {
        'Asset_A': np.random.normal(0.001, 0.02, 1000),
        'Asset_B': np.random.normal(0.0012, 0.022, 1000),
        'Asset_C': np.random.normal(0.0008, 0.018, 1000),
        'Asset_D': np.random.normal(0.0011, 0.019, 1000),
    }
    returns_df = pd.DataFrame(returns_data)

    sharpe_optimizer = SharpeRatioOptimization(returns_df)
    
    optimized_portfolio = sharpe_optimizer.get_optimized_portfolio()
    print(f"Optimized portfolio details:\n{optimized_portfolio}")
