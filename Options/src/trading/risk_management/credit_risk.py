import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreditRisk:
    def __init__(self, counterparty_ratings, exposure):
        """
        Initialize the CreditRisk with counterparty ratings and exposure.

        :param counterparty_ratings: DataFrame containing counterparty ratings with columns ['counterparty', 'rating']
        :param exposure: DataFrame containing exposure with columns ['counterparty', 'exposure']
        """
        self.counterparty_ratings = counterparty_ratings
        self.exposure = exposure
        self.risk_data = self.merge_data()
        logger.info("CreditRisk initialized")

    def merge_data(self):
        """
        Merge counterparty ratings and exposure data.

        :return: DataFrame containing merged data
        """
        merged_data = pd.merge(self.counterparty_ratings, self.exposure, on='counterparty', how='inner')
        logger.info("Merged counterparty ratings and exposure data")
        return merged_data

    def calculate_weighted_average_rating(self):
        """
        Calculate the weighted average credit rating of the portfolio.

        :return: Weighted average credit rating
        """
        ratings = {'AAA': 1, 'AA': 2, 'A': 3, 'BBB': 4, 'BB': 5, 'B': 6, 'CCC': 7, 'CC': 8, 'C': 9, 'D': 10}
        self.risk_data['rating_value'] = self.risk_data['rating'].map(ratings)
        weighted_average_rating = np.average(self.risk_data['rating_value'], weights=self.risk_data['exposure'])
        logger.info(f"Calculated weighted average credit rating: {weighted_average_rating}")
        return weighted_average_rating

    def calculate_default_risk(self):
        """
        Calculate the default risk for each counterparty based on its rating.

        :return: DataFrame with default risk added
        """
        default_probabilities = {'AAA': 0.01, 'AA': 0.02, 'A': 0.05, 'BBB': 0.1, 'BB': 0.2, 'B': 0.4, 'CCC': 0.5, 'CC': 0.7, 'C': 0.9, 'D': 1.0}
        self.risk_data['default_probability'] = self.risk_data['rating'].map(default_probabilities)
        self.risk_data['expected_loss'] = self.risk_data['exposure'] * self.risk_data['default_probability']
        logger.info("Calculated default risk for each counterparty")
        return self.risk_data

    def calculate_total_expected_loss(self):
        """
        Calculate the total expected loss of the portfolio due to credit risk.

        :return: Total expected loss
        """
        self.calculate_default_risk()
        total_expected_loss = self.risk_data['expected_loss'].sum()
        logger.info(f"Calculated total expected loss: {total_expected_loss}")
        return total_expected_loss

# Example usage:
if __name__ == "__main__":
    # Example counterparty ratings
    ratings_data = {
        'counterparty': ['Counterparty_A', 'Counterparty_B', 'Counterparty_C', 'Counterparty_D', 'Counterparty_E'],
        'rating': ['AAA', 'AA', 'A', 'BBB', 'BB']
    }
    counterparty_ratings = pd.DataFrame(ratings_data)

    # Example counterparty exposures
    exposure_data = {
        'counterparty': ['Counterparty_A', 'Counterparty_B', 'Counterparty_C', 'Counterparty_D', 'Counterparty_E'],
        'exposure': [1000000, 500000, 750000, 300000, 200000]
    }
    exposure = pd.DataFrame(exposure_data)

    credit_risk_manager = CreditRisk(counterparty_ratings, exposure)

    weighted_average_rating = credit_risk_manager.calculate_weighted_average_rating()
    print(f"Weighted average credit rating: {weighted_average_rating}")

    default_risk_data = credit_risk_manager.calculate_default_risk()
    print(f"Default risk data:\n{default_risk_data}")

    total_expected_loss = credit_risk_manager.calculate_total_expected_loss()
    print(f"Total expected loss: {total_expected_loss}")
