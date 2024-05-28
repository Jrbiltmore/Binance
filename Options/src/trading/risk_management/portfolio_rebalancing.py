import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PortfolioRebalancing:
    def __init__(self, current_portfolio, target_allocations):
        """
        Initialize the PortfolioRebalancing with current portfolio and target allocations.

        :param current_portfolio: DataFrame containing current portfolio data with columns ['asset', 'value']
        :param target_allocations: Dictionary containing target allocations with assets as keys and target weights as values
        """
        self.current_portfolio = current_portfolio
        self.target_allocations = target_allocations
        logger.info("PortfolioRebalancing initialized")

    def calculate_current_weights(self):
        """
        Calculate the current weights of the portfolio.

        :return: DataFrame containing current weights
        """
        total_value = self.current_portfolio['value'].sum()
        self.current_portfolio['current_weight'] = self.current_portfolio['value'] / total_value
        logger.info(f"Calculated current weights:\n{self.current_portfolio[['asset', 'current_weight']]}")
        return self.current_portfolio[['asset', 'current_weight']]

    def calculate_rebalancing_trades(self):
        """
        Calculate the trades required to rebalance the portfolio to the target allocations.

        :return: DataFrame containing rebalancing trades
        """
        self.calculate_current_weights()
        self.current_portfolio['target_weight'] = self.current_portfolio['asset'].map(self.target_allocations)
        self.current_portfolio['target_value'] = self.current_portfolio['target_weight'] * self.current_portfolio['value'].sum()
        self.current_portfolio['trade_value'] = self.current_portfolio['target_value'] - self.current_portfolio['value']
        logger.info(f"Calculated rebalancing trades:\n{self.current_portfolio[['asset', 'trade_value']]}")
        return self.current_portfolio[['asset', 'trade_value']]

    def execute_rebalancing(self):
        """
        Execute the rebalancing trades and update the portfolio.

        :return: DataFrame containing updated portfolio
        """
        trades = self.calculate_rebalancing_trades()
        self.current_portfolio['value'] += trades['trade_value']
        logger.info(f"Executed rebalancing. Updated portfolio:\n{self.current_portfolio[['asset', 'value']]}")
        return self.current_portfolio[['asset', 'value']]

# Example usage:
if __name__ == "__main__":
    # Example current portfolio data
    current_portfolio_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'value': [300000, 200000, 150000, 250000, 100000]
    }
    current_portfolio_df = pd.DataFrame(current_portfolio_data)

    # Example target allocations
    target_allocations = {
        'Asset_A': 0.2,
        'Asset_B': 0.3,
        'Asset_C': 0.2,
        'Asset_D': 0.2,
        'Asset_E': 0.1
    }

    rebalancing = PortfolioRebalancing(current_portfolio_df, target_allocations)
    
    current_weights = rebalancing.calculate_current_weights()
    print(f"Current weights:\n{current_weights}")

    rebalancing_trades = rebalancing.calculate_rebalancing_trades()
    print(f"Rebalancing trades:\n{rebalancing_trades}")

    updated_portfolio = rebalancing.execute_rebalancing()
    print(f"Updated portfolio:\n{updated_portfolio}")
