import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScenarioAnalysis:
    def __init__(self, portfolio):
        """
        Initialize the ScenarioAnalysis with the portfolio.

        :param portfolio: DataFrame containing portfolio data with columns ['asset', 'value']
        """
        self.portfolio = portfolio
        logger.info("ScenarioAnalysis initialized with portfolio")

    def define_scenario(self, name, changes):
        """
        Define a market scenario with specific changes to asset values.

        :param name: The name of the scenario
        :param changes: Dictionary with assets as keys and percentage changes as values
        :return: Dictionary representing the scenario
        """
        scenario = {
            'name': name,
            'changes': changes
        }
        logger.info(f"Defined scenario '{name}': {changes}")
        return scenario

    def apply_scenario(self, scenario):
        """
        Apply a scenario to the portfolio and calculate the impact on portfolio values.

        :param scenario: Dictionary representing the scenario with 'name' and 'changes'
        :return: DataFrame containing portfolio impact with original and new values
        """
        changes = scenario['changes']
        impact = self.portfolio.copy()
        impact['change'] = impact['asset'].map(changes)
        impact['new_value'] = impact['value'] * (1 + impact['change'] / 100)
        impact['impact'] = impact['new_value'] - impact['value']
        logger.info(f"Applied scenario '{scenario['name']}' to portfolio:\n{impact[['asset', 'value', 'new_value', 'impact']]}")
        return impact[['asset', 'value', 'new_value', 'impact']]

    def calculate_total_impact(self, impact):
        """
        Calculate the total impact of a scenario on the portfolio.

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

    scenario_analysis = ScenarioAnalysis(portfolio_df)

    # Define example scenarios
    scenario1 = scenario_analysis.define_scenario('Market Crash', {
        'Asset_A': -20,
        'Asset_B': -25,
        'Asset_C': -15,
        'Asset_D': -30,
        'Asset_E': -10
    })

    scenario2 = scenario_analysis.define_scenario('Market Rally', {
        'Asset_A': 15,
        'Asset_B': 20,
        'Asset_C': 10,
        'Asset_D': 25,
        'Asset_E': 5
    })

    # Apply scenarios and calculate impacts
    impact1 = scenario_analysis.apply_scenario(scenario1)
    total_impact1 = scenario_analysis.calculate_total_impact(impact1)
    print(f"Total impact of scenario 'Market Crash': {total_impact1}")

    impact2 = scenario_analysis.apply_scenario(scenario2)
    total_impact2 = scenario_analysis.calculate_total_impact(impact2)
    print(f"Total impact of scenario 'Market Rally': {total_impact2}")
