import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PositionSizing:
    def __init__(self, risk_per_trade, account_size):
        """
        Initialize the PositionSizing with risk per trade and account size.

        :param risk_per_trade: Percentage of account size to risk on each trade
        :param account_size: Total size of the trading account
        """
        self.risk_per_trade = risk_per_trade
        self.account_size = account_size
        logger.info("PositionSizing initialized with risk per trade: %s and account size: %s", risk_per_trade, account_size)

    def calculate_position_size(self, stop_loss_amount):
        """
        Calculate the position size based on the risk per trade and stop loss amount.

        :param stop_loss_amount: Amount of loss to set as stop loss for the trade
        :return: Position size
        """
        position_size = (self.risk_per_trade * self.account_size) / stop_loss_amount
        logger.info("Calculated position size: %s for stop loss amount: %s", position_size, stop_loss_amount)
        return position_size

    def assess_position_size(self, position_size, asset_price):
        """
        Assess whether the position size is appropriate based on the asset price and account size.

        :param position_size: Size of the position
        :param asset_price: Current price of the asset
        :return: Boolean indicating whether the position size is appropriate
        """
        total_position_value = position_size * asset_price
        if total_position_value <= self.account_size:
            logger.info("Position size of %s is appropriate for asset price %s", position_size, asset_price)
            return True
        else:
            logger.warning("Position size of %s is too large for asset price %s", position_size, asset_price)
            return False

# Example usage:
if __name__ == "__main__":
    # Example account size and risk per trade
    account_size = 100000  # Example account size of 100,000
    risk_per_trade = 0.01  # Example risk per trade of 1%

    position_sizing = PositionSizing(risk_per_trade, account_size)
    
    # Example stop loss amount
    stop_loss_amount = 500  # Example stop loss amount of 500

    position_size = position_sizing.calculate_position_size(stop_loss_amount)
    print(f"Calculated position size: {position_size}")

    # Example asset price
    asset_price = 50  # Example asset price of 50

    is_appropriate = position_sizing.assess_position_size(position_size, asset_price)
    print(f"Is the position size appropriate? {is_appropriate}")
