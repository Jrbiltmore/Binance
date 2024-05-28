import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Diversification:
    def __init__(self, portfolio):
        """
        Initialize the Diversification class with portfolio data.

        :param portfolio: DataFrame containing portfolio data with columns ['asset', 'value']
        """
        self.portfolio = portfolio
        logger.info("Diversification initialized with portfolio:\n%s", self.portfolio)

    def calculate_herfindahl_index(self):
        """
        Calculate the Herfindahl-Hirschman Index (HHI) for the portfolio.

        :return: Herfindahl-Hirschman Index (HHI)
        """
        total_value = self.portfolio['value'].sum()
        self.portfolio['weight'] = self.portfolio['value'] / total_value
        hhi = (self.portfolio['weight'] ** 2).sum()
        logger.info(f"Calculated Herfindahl-Hirschman Index (HHI): {hhi}")
        return hhi

    def calculate_shannon_entropy(self):
        """
        Calculate the Shannon Entropy for the portfolio.

        :return: Shannon Entropy
        """
        total_value = self.portfolio['value'].sum()
        self.portfolio['weight'] = self.portfolio['value'] / total_value
        shannon_entropy = -np.sum(self.portfolio['weight'] * np.log(self.portfolio['weight']))
        logger.info(f"Calculated Shannon Entropy: {shannon_entropy}")
        return shannon_entropy

    def calculate_diversification_ratio(self):
        """
        Calculate the diversification ratio for the portfolio.

        :return: Diversification Ratio
        """
        total_value = self.portfolio['value'].sum()
        average_weight = 1 / len(self.portfolio)
        self.portfolio['weight'] = self.portfolio['value'] / total_value
        diversification_ratio = np.sum(self.portfolio['weight']) / average_weight
        logger.info(f"Calculated Diversification Ratio: {diversification_ratio}")
        return diversification_ratio

    def assess_diversification(self):
        """
        Assess the diversification of the portfolio using multiple metrics.

        :return: Dictionary containing diversification metrics
        """
        hhi = self.calculate_herfindahl_index()
        shannon_entropy = self.calculate_shannon_entropy()
        diversification_ratio = self.calculate_diversification_ratio()

        metrics = {
            'Herfindahl-Hirschman Index (HHI)': hhi,
            'Shannon Entropy': shannon_entropy,
            'Diversification Ratio': diversification_ratio
        }

        logger.info(f"Diversification assessment metrics: {metrics}")
        return metrics

# Example usage:
if __name__ == "__main__":
    # Example portfolio data
    portfolio_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'value': [300000, 200000, 150000, 250000, 100000]
    }
    portfolio = pd.DataFrame(portfolio_data)

    diversification = Diversification(portfolio)
    diversification_metrics = diversification.assess_diversification()
    print(diversification_metrics)
