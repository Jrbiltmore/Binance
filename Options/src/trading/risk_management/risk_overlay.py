import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskOverlay:
    def __init__(self, portfolio, risk_metrics):
        """
        Initialize the RiskOverlay with portfolio and risk metrics.

        :param portfolio: DataFrame containing portfolio data with columns ['asset', 'value']
        :param risk_metrics: DataFrame containing risk metrics with columns ['asset', 'risk_metric']
        """
        self.portfolio = portfolio
        self.risk_metrics = risk_metrics
        self.merged_data = self.merge_data()
        logger.info("RiskOverlay initialized with portfolio and risk metrics")

    def merge_data(self):
        """
        Merge portfolio data with risk metrics.

        :return: DataFrame containing merged data
        """
        merged_data = pd.merge(self.portfolio, self.risk_metrics, on='asset', how='inner')
        logger.info("Merged portfolio data with risk metrics")
        return merged_data

    def calculate_risk_adjusted_values(self):
        """
        Calculate risk-adjusted values for the portfolio.

        :return: DataFrame containing risk-adjusted values
        """
        self.merged_data['risk_adjusted_value'] = self.merged_data['value'] / self.merged_data['risk_metric']
        logger.info(f"Calculated risk-adjusted values:\n{self.merged_data[['asset', 'risk_adjusted_value']]}")
        return self.merged_data[['asset', 'risk_adjusted_value']]

    def adjust_positions(self, target_risk_level):
        """
        Adjust positions based on the target risk level.

        :param target_risk_level: The target risk level for the portfolio
        :return: DataFrame containing adjusted positions
        """
        total_risk_adjusted_value = self.merged_data['risk_adjusted_value'].sum()
        self.merged_data['adjusted_value'] = self.merged_data['risk_adjusted_value'] / total_risk_adjusted_value * target_risk_level
        self.merged_data['trade_value'] = self.merged_data['adjusted_value'] - self.merged_data['value']
        logger.info(f"Adjusted positions based on target risk level {target_risk_level}:\n{self.merged_data[['asset', 'adjusted_value', 'trade_value']]}")
        return self.merged_data[['asset', 'adjusted_value', 'trade_value']]

# Example usage:
if __name__ == "__main__":
    # Example portfolio data
    portfolio_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'value': [300000, 200000, 150000, 250000, 100000]
    }
    portfolio_df = pd.DataFrame(portfolio_data)

    # Example risk metrics data
    risk_metrics_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'risk_metric': [0.8, 1.2, 0.6, 1.0, 1.5]
    }
    risk_metrics_df = pd.DataFrame(risk_metrics_data)

    risk_overlay = RiskOverlay(portfolio_df, risk_metrics_df)
    
    risk_adjusted_values = risk_overlay.calculate_risk_adjusted_values()
    print(f"Risk-adjusted values:\n{risk_adjusted_values}")

    target_risk_level = 1000000  # Example target risk level
    adjusted_positions = risk_overlay.adjust_positions(target_risk_level)
    print(f"Adjusted positions:\n{adjusted_positions}")
