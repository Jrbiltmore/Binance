import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionCostAnalysis:
    def __init__(self, trades, costs):
        """
        Initialize the TransactionCostAnalysis with trades and costs data.

        :param trades: DataFrame containing trade data with columns ['asset', 'quantity', 'price']
        :param costs: Dictionary containing cost details with keys ['commission', 'slippage', 'taxes']
        """
        self.trades = trades
        self.costs = costs
        logger.info("TransactionCostAnalysis initialized with trades and costs")

    def calculate_commission(self):
        """
        Calculate the total commission cost for the trades.

        :return: Total commission cost
        """
        total_commission = self.trades['quantity'] * self.trades['price'] * self.costs['commission']
        self.trades['commission'] = total_commission
        total_commission_sum = total_commission.sum()
        logger.info(f"Calculated total commission cost: {total_commission_sum}")
        return total_commission_sum

    def calculate_slippage(self):
        """
        Calculate the total slippage cost for the trades.

        :return: Total slippage cost
        """
        total_slippage = self.trades['quantity'] * self.trades['price'] * self.costs['slippage']
        self.trades['slippage'] = total_slippage
        total_slippage_sum = total_slippage.sum()
        logger.info(f"Calculated total slippage cost: {total_slippage_sum}")
        return total_slippage_sum

    def calculate_taxes(self):
        """
        Calculate the total tax cost for the trades.

        :return: Total tax cost
        """
        total_taxes = self.trades['quantity'] * self.trades['price'] * self.costs['taxes']
        self.trades['taxes'] = total_taxes
        total_taxes_sum = total_taxes.sum()
        logger.info(f"Calculated total tax cost: {total_taxes_sum}")
        return total_taxes_sum

    def total_transaction_cost(self):
        """
        Calculate the total transaction cost for the trades.

        :return: Total transaction cost
        """
        total_cost = self.calculate_commission() + self.calculate_slippage() + self.calculate_taxes()
        logger.info(f"Calculated total transaction cost: {total_cost}")
        return total_cost

    def impact_on_trade(self):
        """
        Calculate the impact of transaction costs on each trade.

        :return: DataFrame with trade impact details
        """
        self.trades['total_cost'] = self.trades['commission'] + self.trades['slippage'] + self.trades['taxes']
        self.trades['net_price'] = self.trades['price'] - (self.trades['total_cost'] / self.trades['quantity'])
        logger.info(f"Calculated impact of transaction costs on trades:\n{self.trades[['asset', 'quantity', 'price', 'total_cost', 'net_price']]}")
        return self.trades[['asset', 'quantity', 'price', 'total_cost', 'net_price']]

# Example usage:
if __name__ == "__main__":
    # Example trades data
    trades_data = {
        'asset': ['Asset_A', 'Asset_B', 'Asset_C', 'Asset_D', 'Asset_E'],
        'quantity': [100, 200, 150, 250, 300],
        'price': [50, 60, 55, 65, 70]
    }
    trades_df = pd.DataFrame(trades_data)

    # Example costs data
    costs_data = {
        'commission': 0.001,  # 0.1% commission
        'slippage': 0.0005,   # 0.05% slippage
        'taxes': 0.002        # 0.2% taxes
    }

    tca = TransactionCostAnalysis(trades_df, costs_data)
    
    total_cost = tca.total_transaction_cost()
    print(f"Total transaction cost: {total_cost}")

    trade_impact = tca.impact_on_trade()
    print(f"Impact of transaction costs on trades:\n{trade_impact}")
