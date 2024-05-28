import logging
import time
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HFTRiskControls:
    def __init__(self, position_limits, trade_limits, time_window=60):
        """
        Initialize the HFTRiskControls with position and trade limits.

        :param position_limits: Dictionary with position limits for each asset
        :param trade_limits: Dictionary with trade limits for each asset
        :param time_window: Time window in seconds for trade limits (default is 60 seconds)
        """
        self.position_limits = position_limits
        self.trade_limits = trade_limits
        self.time_window = time_window
        self.positions = defaultdict(float)
        self.trade_counts = defaultdict(int)
        self.trade_timestamps = defaultdict(list)
        logger.info("HFTRiskControls initialized")

    def update_position(self, asset, quantity):
        """
        Update the position for a given asset.

        :param asset: The asset being traded
        :param quantity: The quantity of the trade
        :return: Boolean indicating whether the position is within limits
        """
        self.positions[asset] += quantity
        if abs(self.positions[asset]) > self.position_limits[asset]:
            logger.warning(f"Position limit exceeded for {asset}. Current position: {self.positions[asset]}, Limit: {self.position_limits[asset]}")
            return False
        logger.info(f"Updated position for {asset}. Current position: {self.positions[asset]}")
        return True

    def update_trade_count(self, asset):
        """
        Update the trade count for a given asset.

        :param asset: The asset being traded
        :return: Boolean indicating whether the trade count is within limits
        """
        current_time = time.time()
        self.trade_timestamps[asset].append(current_time)
        self.trade_timestamps[asset] = [timestamp for timestamp in self.trade_timestamps[asset] if current_time - timestamp <= self.time_window]
        self.trade_counts[asset] = len(self.trade_timestamps[asset])
        if self.trade_counts[asset] > self.trade_limits[asset]:
            logger.warning(f"Trade limit exceeded for {asset}. Current trade count: {self.trade_counts[asset]}, Limit: {self.trade_limits[asset]}")
            return False
        logger.info(f"Updated trade count for {asset}. Current trade count: {self.trade_counts[asset]}")
        return True

    def check_risk_controls(self, asset, quantity):
        """
        Check all risk controls for a given trade.

        :param asset: The asset being traded
        :param quantity: The quantity of the trade
        :return: Boolean indicating whether all risk controls are within limits
        """
        position_ok = self.update_position(asset, quantity)
        trade_count_ok = self.update_trade_count(asset)
        return position_ok and trade_count_ok

# Example usage:
if __name__ == "__main__":
    # Example position and trade limits
    position_limits = {'Asset_A': 1000, 'Asset_B': 2000}
    trade_limits = {'Asset_A': 10, 'Asset_B': 20}

    hft_risk_controls = HFTRiskControls(position_limits, trade_limits)

    # Simulate trades
    trades = [
        ('Asset_A', 100),
        ('Asset_A', 200),
        ('Asset_B', 500),
        ('Asset_A', -50),
        ('Asset_A', 700),
        ('Asset_B', -1000),
        ('Asset_A', 100),
        ('Asset_B', 500),
        ('Asset_A', -200),
        ('Asset_A', 300),
        ('Asset_B', 200)
    ]

    for asset, quantity in trades:
        if not hft_risk_controls.check_risk_controls(asset, quantity):
            print(f"Risk control violation for trade: {asset}, {quantity}")
        else:
            print(f"Trade executed: {asset}, {quantity}")
