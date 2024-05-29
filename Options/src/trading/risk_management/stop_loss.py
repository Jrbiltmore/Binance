import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StopLoss:
    def __init__(self, percentage):
        """
        Initialize the StopLoss with a stop-loss percentage.

        :param percentage: Percentage to set as the stop-loss threshold
        """
        self.percentage = percentage
        logger.info(f"StopLoss initialized with stop-loss percentage: {percentage}%")

    def set_stop_loss(self, entry_price):
        """
        Set the stop-loss price based on the entry price and stop-loss percentage.

        :param entry_price: The price at which the asset was bought
        :return: The stop-loss price
        """
        stop_loss_price = entry_price * (1 - self.percentage / 100)
        logger.info(f"Set stop-loss price at: {stop_loss_price} for entry price: {entry_price}")
        return stop_loss_price

    def check_stop_loss(self, current_price, stop_loss_price):
        """
        Check if the current price has triggered the stop-loss.

        :param current_price: The current price of the asset
        :param stop_loss_price: The stop-loss price
        :return: Boolean indicating whether the stop-loss has been triggered
        """
        if current_price <= stop_loss_price:
            logger.info(f"Stop-loss triggered: current price {current_price} <= stop-loss price {stop_loss_price}")
            return True
        else:
            logger.info(f"Stop-loss not triggered: current price {current_price} > stop-loss price {stop_loss_price}")
            return False

# Example usage:
if __name__ == "__main__":
    # Example stop-loss percentage
    stop_loss_percentage = 10  # 10%

    stop_loss = StopLoss(stop_loss_percentage)
    
    # Example entry price
    entry_price = 100  # Example entry price of 100

    stop_loss_price = stop_loss.set_stop_loss(entry_price)
    print(f"Stop-loss price: {stop_loss_price}")

    # Example current prices to check
    current_prices = [95, 85, 105, 90]

    for price in current_prices:
        triggered = stop_loss.check_stop_loss(price, stop_loss_price)
        print(f"Current price: {price}, Stop-loss triggered: {triggered}")
