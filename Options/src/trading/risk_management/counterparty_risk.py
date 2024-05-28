import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CounterpartyRisk:
    def __init__(self, counterparty_exposures):
        """
        Initialize the CounterpartyRisk with counterparty exposures.

        :param counterparty_exposures: DataFrame containing counterparty exposures with columns ['counterparty', 'exposure']
        """
        self.counterparty_exposures = counterparty_exposures
        logger.info("CounterpartyRisk initialized with exposures:\n%s", self.counterparty_exposures)

    def calculate_total_exposure(self):
        """
        Calculate the total exposure to all counterparties.

        :return: Total exposure
        """
        total_exposure = self.counterparty_exposures['exposure'].sum()
        logger.info(f"Calculated total exposure: {total_exposure}")
        return total_exposure

    def calculate_average_exposure(self):
        """
        Calculate the average exposure per counterparty.

        :return: Average exposure
        """
        average_exposure = self.counterparty_exposures['exposure'].mean()
        logger.info(f"Calculated average exposure: {average_exposure}")
        return average_exposure

    def calculate_exposure_to_counterparty(self, counterparty):
        """
        Calculate the exposure to a specific counterparty.

        :param counterparty: The counterparty to calculate exposure for
        :return: Exposure to the specified counterparty
        """
        exposure = self.counterparty_exposures[self.counterparty_exposures['counterparty'] == counterparty]['exposure'].sum()
        logger.info(f"Calculated exposure to {counterparty}: {exposure}")
        return exposure

    def calculate_top_n_exposures(self, n=5):
        """
        Calculate the top N exposures to counterparties.

        :param n: Number of top exposures to calculate
        :return: DataFrame containing the top N exposures
        """
        top_exposures = self.counterparty_exposures.nlargest(n, 'exposure')
        logger.info(f"Calculated top {n} exposures:\n%s", top_exposures)
        return top_exposures

    def calculate_exposure_distribution(self):
        """
        Calculate the distribution of exposures to counterparties.

        :return: Series containing the exposure distribution
        """
        exposure_distribution = self.counterparty_exposures['exposure'].value_counts(normalize=True)
        logger.info("Calculated exposure distribution:\n%s", exposure_distribution)
        return exposure_distribution

# Example usage:
if __name__ == "__main__":
    # Example counterparty exposures
    data = {
        'counterparty': ['Counterparty_A', 'Counterparty_B', 'Counterparty_C', 'Counterparty_D', 'Counterparty_E'],
        'exposure': [1000000, 500000, 750000, 300000, 200000]
    }
    counterparty_exposures = pd.DataFrame(data)

    risk_manager = CounterpartyRisk(counterparty_exposures)

    total_exposure = risk_manager.calculate_total_exposure()
    print(f"Total exposure: {total_exposure}")

    average_exposure = risk_manager.calculate_average_exposure()
    print(f"Average exposure: {average_exposure}")

    exposure_to_b = risk_manager.calculate_exposure_to_counterparty('Counterparty_B')
    print(f"Exposure to Counterparty_B: {exposure_to_b}")

    top_exposures = risk_manager.calculate_top_n_exposures()
    print(f"Top exposures:\n{top_exposures}")

    exposure_distribution = risk_manager.calculate_exposure_distribution()
    print(f"Exposure distribution:\n{exposure_distribution}")
