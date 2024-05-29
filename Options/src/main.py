import logging
import time
from utils.config import Config
from utils.logger import setup_logger
from utils.notifier import Notifier
from trading.data_fetcher import DataFetcher
from trading.data_processor import DataProcessor
from trading.execution import Execution
from trading.strategy import Strategy
from trading.risk_management import RiskManagement

# Set up logging
logger = setup_logger('binance_options_trading', 'binance_options_trading.log')

def main():
    """
    Main function to initialize and run the Binance Options trading system.
    """
    logger.info("Starting Binance Options trading system")

    # Load configuration
    config = Config('config.json')
    
    # Initialize components
    api_client = None  # Placeholder for the actual API client instance
    notifier = Notifier(email_config=config.get('email'), sms_config=config.get('sms'))

    data_fetcher = DataFetcher(api_client)
    data_processor = DataProcessor(data_fetcher)
    execution = Execution(api_client)
    risk_management = RiskManagement()

    # Initialize strategies
    strategy = Strategy(data_processor, execution, risk_management)

    symbol = 'BTCUSDT'
    interval = config.get('trading_interval', 60)  # Interval in seconds

    try:
        while True:
            logger.info("Running trading strategies")

            # Execute strategies
            strategy.moving_average_strategy(symbol)
            strategy.rsi_strategy(symbol)

            logger.info("Trading strategies execution completed")

            # Sleep for the configured interval
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Stopping Binance Options trading system")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        notifier.send_email(
            to_address=config.get('alert_email'),
            subject='Trading System Error',
            body=f"An error occurred in the trading system: {e}"
        )

if __name__ == "__main__":
    main()
