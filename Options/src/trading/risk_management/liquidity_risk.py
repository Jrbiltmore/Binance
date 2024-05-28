import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiquidityRisk:
    def __init__(self, market_data, portfolio):
        """
        Initialize the LiquidityRisk with market data and portfolio.

        :param market_data: DataFrame containing market data with columns ['asset', 'volume', 'spread']
        :param portfolio: DataFrame containing portfolio data with columns ['asset', 'value']
        """
        self.market_data = market_data
        self.portfolio = portfolio
        self.liquidity_data = self.merge_data()
        logger.info("LiquidityRisk initialized with market data and portfolio")

    def merge_data(self):
        """
        Merge market data and portfolio data.

        :return: DataFrame containing merged data
        """
        merged_data = pd.merge(self.portfolio, self.market_data, on='asset', how='inner')
        logger.info("Merged market data and portfolio data")
        return merged_data

    def calculate_liquidity_ratio(self):
        """
        Calculate the liquidity ratio for each asset in the portfolio.

        :return: DataFrame containing liquidity ratios
        """
        self.liquidity_data['liquidity_ratio'] = self.liquidity_data['value'] / (self.liquidity_data['volume'] * self.liquidity_data['spread'])
        logger.info(f"Calculated liquidity ratios:\n{self.liquidity_data[['asset', 'liquidity_ratio']]}")
        return self.liquidity_data[['asset', 'liquidity_ratio']]

    def calculate_portfolio_liquidity_risk(self):
        """
        Calculate the overall liquidity risk of the portfolio.

        :return: Liquidity risk score
        """
        self.calculate_liquidity_ratio()
        liquidity_risk_score = np.average(self.liquidity_data['liquidity_ratio'], weights=self.liquidity_data['value'])
        logger.info(f"Calculated portfolio liquidity risk score: {liquidity_risk_score}")
        return liquidity_risk_score

    def assess_liquidity_risk(self):
        """
        Assess the liquidity risk of the portfolio using liquidity ratios and overall liquidity risk score.

        :return: Dictionary containing liquidity risk assessment
        """
        liquidity_ratios = self.calculate_liquidity_ratio()
        portfolio_liquidity_risk = self.calculate_portfolio_liquidity_risk()
        
        liquidity_risk_assessment = {
            'liquidity_ratios': liquidity_ratios,
            'portfolio_liquidity_risk': portfolio_liquidity_risk
        }
        
        logger.info(f"Liquidity risk assessment: {liquidity_risk_assessment}")
        return liquidity_risk_assessment

# Example usage:
if __name__ == "__main__":
    # Example market data
    market_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'volume': [100000, 150000, 120000, 80000, 60000],
        'spread': [0.01, 0.015, 0.02, 0.025, 0.03]
    }
    market_data_df = pd.DataFrame(market_data)

    # Example portfolio data
    portfolio_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'value': [300000, 200000, 150000, 250000, 100000]
    }
    portfolio_df = pd.DataFrame(portfolio_data)

    liquidity_risk_manager = LiquidityRisk(market_data_df, portfolio_df)
    liquidity_risk_assessment = liquidity_risk_manager.assess_liquidity_risk()
    print(f"Liquidity risk assessment: {liquidity_risk_assessment}")
