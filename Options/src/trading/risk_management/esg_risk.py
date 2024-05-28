import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ESGRisk:
    def __init__(self, esg_data, portfolio):
        """
        Initialize the ESGRisk with ESG data and portfolio.

        :param esg_data: DataFrame containing ESG scores with columns ['asset', 'environmental', 'social', 'governance']
        :param portfolio: DataFrame containing portfolio data with columns ['asset', 'value']
        """
        self.esg_data = esg_data
        self.portfolio = portfolio
        self.esg_portfolio = self.merge_data()
        logger.info("ESGRisk initialized with ESG and portfolio data")

    def merge_data(self):
        """
        Merge ESG data and portfolio data.

        :return: DataFrame containing merged data
        """
        merged_data = pd.merge(self.portfolio, self.esg_data, on='asset', how='inner')
        logger.info("Merged ESG and portfolio data")
        return merged_data

    def calculate_weighted_esg_scores(self):
        """
        Calculate the weighted ESG scores for the portfolio.

        :return: Dictionary containing weighted ESG scores
        """
        total_value = self.esg_portfolio['value'].sum()
        self.esg_portfolio['weight'] = self.esg_portfolio['value'] / total_value
        weighted_scores = {
            'environmental': np.average(self.esg_portfolio['environmental'], weights=self.esg_portfolio['weight']),
            'social': np.average(self.esg_portfolio['social'], weights=self.esg_portfolio['weight']),
            'governance': np.average(self.esg_portfolio['governance'], weights=self.esg_portfolio['weight'])
        }
        logger.info(f"Calculated weighted ESG scores: {weighted_scores}")
        return weighted_scores

    def assess_esg_risk(self):
        """
        Assess the ESG risk of the portfolio using weighted ESG scores.

        :return: Dictionary containing ESG risk assessment
        """
        weighted_scores = self.calculate_weighted_esg_scores()
        esg_risk_assessment = {
            'environmental_risk': 1 - weighted_scores['environmental'],
            'social_risk': 1 - weighted_scores['social'],
            'governance_risk': 1 - weighted_scores['governance']
        }
        logger.info(f"ESG risk assessment: {esg_risk_assessment}")
        return esg_risk_assessment

# Example usage:
if __name__ == "__main__":
    # Example ESG data
    esg_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'environmental': [0.8, 0.6, 0.9, 0.7, 0.5],
        'social': [0.7, 0.8, 0.6, 0.9, 0.6],
        'governance': [0.9, 0.7, 0.8, 0.6, 0.5]
    }
    esg_data_df = pd.DataFrame(esg_data)

    # Example portfolio data
    portfolio_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'value': [300000, 200000, 150000, 250000, 100000]
    }
    portfolio_df = pd.DataFrame(portfolio_data)

    esg_risk_manager = ESGRisk(esg_data_df, portfolio_df)
    weighted_esg_scores = esg_risk_manager.calculate_weighted_esg_scores()
    print(f"Weighted ESG scores: {weighted_esg_scores}")

    esg_risk_assessment = esg_risk_manager.assess_esg_risk()
    print(f"ESG risk assessment: {esg_risk_assessment}")
