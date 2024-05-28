import numpy as np
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DrawdownControl:
    def __init__(self, returns):
        """
        Initialize the DrawdownControl with returns data.

        :param returns: Series of portfolio returns
        """
        self.returns = returns
        logger.info("DrawdownControl initialized with returns data")

    def calculate_drawdown(self):
        """
        Calculate the drawdown series from the returns.

        :return: Series of drawdowns
        """
        cumulative_returns = (1 + self.returns).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        logger.info("Calculated drawdown series")
        return drawdown

    def calculate_max_drawdown(self):
        """
        Calculate the maximum drawdown from the returns.

        :return: Maximum drawdown value
        """
        drawdown = self.calculate_drawdown()
        max_drawdown = drawdown.min()
        logger.info(f"Calculated maximum drawdown: {max_drawdown}")
        return max_drawdown

    def calculate_drawdown_duration(self):
        """
        Calculate the duration of the maximum drawdown period.

        :return: Duration of the maximum drawdown period in terms of number of periods
        """
        drawdown = self.calculate_drawdown()
        end_period = drawdown.idxmin()
        start_period = (drawdown[:end_period][drawdown[:end_period] == 0]).idxmax()
        duration = (end_period - start_period).days
        logger.info(f"Calculated drawdown duration: {duration} days")
        return duration

# Example usage:
if __name__ == "__main__":
    # Example portfolio returns
    portfolio_returns = pd.Series(np.random.normal(0, 0.01, 1000))

    drawdown_control = DrawdownControl(portfolio_returns)
    
    drawdown_series = drawdown_control.calculate_drawdown()
    print(f"Drawdown series:\n{drawdown_series}")

    max_drawdown = drawdown_control.calculate_max_drawdown()
    print(f"Maximum drawdown: {max_drawdown}")

    drawdown_duration = drawdown_control.calculate_drawdown_duration()
    print(f"Drawdown duration: {drawdown_duration} days")
