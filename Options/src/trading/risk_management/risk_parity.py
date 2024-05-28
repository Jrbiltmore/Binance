import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskParity:
    def __init__(self, assets, cov_matrix):
        """
        Initialize the RiskParity with assets and their covariance matrix.

        :param assets: List of assets
        :param cov_matrix: DataFrame containing the covariance matrix of asset returns
        """
        self.assets = assets
        self.cov_matrix = cov_matrix
        self.risk_parity_weights = self.calculate_risk_parity_weights()
        logger.info("RiskParity initialized with assets and covariance matrix")

    def calculate_asset_risks(self):
        """
        Calculate the individual asset risks based on the covariance matrix.

        :return: Series containing asset risks
        """
        asset_risks = np.sqrt(np.diag(self.cov_matrix))
        asset_risks_series = pd.Series(asset_risks, index=self.assets)
        logger.info(f"Calculated asset risks:\n{asset_risks_series}")
        return asset_risks_series

    def calculate_risk_parity_weights(self):
        """
        Calculate the risk parity weights for the portfolio.

        :return: Series containing risk parity weights
        """
        asset_risks = self.calculate_asset_risks()
        inverse_risks = 1 / asset_risks
        risk_parity_weights = inverse_risks / inverse_risks.sum()
        risk_parity_weights_series = pd.Series(risk_parity_weights, index=self.assets)
        logger.info(f"Calculated risk parity weights:\n{risk_parity_weights_series}")
        return risk_parity_weights_series

    def calculate_portfolio_risk(self):
        """
        Calculate the overall portfolio risk based on risk parity weights.

        :return: Portfolio risk
        """
        weights = self.risk_parity_weights.values
        portfolio_variance = np.dot(weights.T, np.dot(self.cov_matrix, weights))
        portfolio_risk = np.sqrt(portfolio_variance)
        logger.info(f"Calculated portfolio risk: {portfolio_risk}")
        return portfolio_risk

# Example usage:
if __name__ == "__main__":
    # Example assets and covariance matrix
    assets = ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D']
    cov_matrix_data = {
        'Asset_A': [0.1, 0.02, 0.03, 0.04],
        'Asset_B': [0.02, 0.2, 0.05, 0.06],
        'Asset_C': [0.03, 0.05, 0.15, 0.07],
        'Asset_D': [0.04, 0.06, 0.07, 0.25]
    }
    cov_matrix_df = pd.DataFrame(cov_matrix_data, index=assets)

    risk_parity = RiskParity(assets, cov_matrix_df)
    
    asset_risks = risk_parity.calculate_asset_risks()
    print(f"Asset risks:\n{asset_risks}")

    risk_parity_weights = risk_parity.calculate_risk_parity_weights()
    print(f"Risk parity weights:\n{risk_parity_weights}")

    portfolio_risk = risk_parity.calculate_portfolio_risk()
    print(f"Portfolio risk: {portfolio_risk}")
