import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StressTesting:
    def __init__(self, portfolio):
        """
        Initialize the StressTesting with the portfolio.

        :param portfolio: DataFrame containing portfolio data with columns ['asset', 'value']
        """
        self.portfolio = portfolio
        logger.info("StressTesting initialized with portfolio")

    def define_stress_scenario(self, name, changes):
        """
        Define a stress test scenario with specific changes to asset values.

        :param name: The name of the scenario
        :param changes: Dictionary with assets as keys and percentage changes as values
        :return: Dictionary representing the stress test scenario
        """
        scenario = {
            'name': name,
            'changes': changes
        }
        logger.info(f"Defined stress scenario '{name}': {changes}")
        return scenario

    def apply_stress_scenario(self, scenario):
        """
        Apply a stress test scenario to the portfolio and calculate the impact on portfolio values.

        :param scenario: Dictionary representing the scenario with 'name' and 'changes'
        :return: DataFrame containing portfolio impact with original and new values
        """
        changes = scenario['changes']
        impact = self.portfolio.copy()
        impact['change'] = impact['asset'].map(changes)
        impact['new_value'] = impact['value'] * (1 + impact['change'] / 100)
        impact['impact'] = impact['new_value'] - impact['value']
        logger.info(f"Applied stress scenario '{scenario['name']}' to portfolio:\n{impact[['asset', 'value', 'new_value', 'impact']]}")
        return impact[['asset', 'value', 'new_value', 'impact']]

    def calculate_total_impact(self, impact):
        """
        Calculate the total impact of a stress test scenario on the portfolio.

        :param impact: DataFrame containing the impact of the scenario on the portfolio
        :return: Total impact value
        """
        total_impact = impact['impact'].sum()
        logger.info(f"Calculated total impact on portfolio: {total_impact}")
        return total_impact

# Example usage:
if __name__ == "__main__":
    # Example portfolio data
    portfolio_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'value': [300000, 200000, 150000, 250000, 100000]
    }
    portfolio_df = pd.DataFrame(portfolio_data)

    stress_testing = StressTesting(portfolio_df)

    # Define example stress scenarios
    scenario1 = stress_testing.define_stress_scenario('Market Crash', {
        'Asset_A': -20,
        'Asset_B': -25,
        'Asset_C': -15,
        'Asset_D': -30,
        'Asset_E': -10
    })

    scenario2 = stress_testing.define_stress_scenario('Market Rally', {
        'Asset_A': 15,
        'Asset_B': 20,
        'Asset_C': 10,
        'Asset_D': 25,
        'Asset_E': 5
    })

    # Apply stress scenarios and calculate impacts
    impact1 = stress_testing.apply_stress_scenario(scenario1)
    total_impact1 = stress_testing.calculate_total_impact(impact1)
    print(f"Total impact of scenario 'Market Crash': {total_impact1}")

    impact2 = stress_testing.apply_stress_scenario(scenario2)
    total_impact2 = stress_testing.calculate_total_impact(impact2)
    print(f"Total impact of scenario 'Market Rally': {total_impact2}")
