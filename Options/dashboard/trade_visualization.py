import matplotlib.pyplot as plt
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradeVisualization:
    def __init__(self, trade_data):
        """
        Initialize the TradeVisualization with trade data.

        :param trade_data: DataFrame containing trade data with columns ['timestamp', 'price', 'quantity', 'side']
        """
        self.trade_data = trade_data
        logger.info("TradeVisualization initialized")

    def plot_trade_history(self):
        """
        Plot the trade history with buy and sell signals.
        """
        try:
            buy_signals = self.trade_data[self.trade_data['side'] == 'buy']
            sell_signals = self.trade_data[self.trade_data['side'] == 'sell']

            plt.figure(figsize=(14, 7))
            plt.plot(self.trade_data['timestamp'], self.trade_data['price'], label='Price', color='blue')
            plt.scatter(buy_signals['timestamp'], buy_signals['price'], marker='^', color='green', label='Buy', alpha=1)
            plt.scatter(sell_signals['timestamp'], sell_signals['price'], marker='v', color='red', label='Sell', alpha=1)
            plt.title('Trade History')
            plt.xlabel('Timestamp')
            plt.ylabel('Price')
            plt.legend()
            plt.grid()
            plt.show()

            logger.info("Trade history plotted successfully")
        except Exception as e:
            logger.error(f"Error plotting trade history: {e}")
            raise

    def plot_portfolio_value(self, portfolio_values):
        """
        Plot the portfolio value over time.

        :param portfolio_values: DataFrame containing portfolio values with columns ['timestamp', 'value']
        """
        try:
            plt.figure(figsize=(14, 7))
            plt.plot(portfolio_values['timestamp'], portfolio_values['value'], label='Portfolio Value', color='blue')
            plt.title('Portfolio Value Over Time')
            plt.xlabel('Timestamp')
            plt.ylabel('Portfolio Value')
            plt.legend()
            plt.grid()
            plt.show()

            logger.info("Portfolio value plotted successfully")
        except Exception as e:
            logger.error(f"Error plotting portfolio value: {e}")
            raise

# Example usage:
if __name__ == "__main__":
    # Mock trade data
    trade_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2022-01-01', periods=100, freq='D'),
        'price': pd.Series(pd.np.random.randn(100).cumsum() + 100),
        'quantity': pd.Series(pd.np.random.randint(1, 10, size=100)),
        'side': pd.Series(pd.np.random.choice(['buy', 'sell'], size=100))
    })

    # Mock portfolio values
    portfolio_values = pd.DataFrame({
        'timestamp': pd.date_range(start='2022-01-01', periods=100, freq='D'),
        'value': pd.Series(pd.np.random.randn(100).cumsum() + 1000)
    })

    trade_viz = TradeVisualization(trade_data)
    trade_viz.plot_trade_history()
    trade_viz.plot_portfolio_value(portfolio_values)
