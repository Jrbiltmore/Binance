import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegulatoryCompliance:
    def __init__(self):
        """
        Initialize the RegulatoryCompliance class.
        """
        self.compliance_log = []
        logger.info("RegulatoryCompliance initialized")

    def log_compliance_check(self, rule, status, details=""):
        """
        Log the result of a compliance check.

        :param rule: The name of the compliance rule checked
        :param status: The status of the compliance check ('PASS' or 'FAIL')
        :param details: Additional details about the compliance check
        """
        log_entry = {
            'timestamp': datetime.now(),
            'rule': rule,
            'status': status,
            'details': details
        }
        self.compliance_log.append(log_entry)
        logger.info(f"Logged compliance check: {log_entry}")

    def check_trade_limit(self, trade_volume, max_trade_volume):
        """
        Check if the trade volume complies with the maximum allowed trade volume.

        :param trade_volume: The volume of the trade
        :param max_trade_volume: The maximum allowed trade volume
        :return: Boolean indicating compliance status
        """
        if trade_volume <= max_trade_volume:
            self.log_compliance_check('Trade Volume Limit', 'PASS', f"Trade volume: {trade_volume}, Limit: {max_trade_volume}")
            return True
        else:
            self.log_compliance_check('Trade Volume Limit', 'FAIL', f"Trade volume: {trade_volume}, Limit: {max_trade_volume}")
            return False

    def check_position_limit(self, position_value, max_position_value):
        """
        Check if the position value complies with the maximum allowed position value.

        :param position_value: The value of the position
        :param max_position_value: The maximum allowed position value
        :return: Boolean indicating compliance status
        """
        if position_value <= max_position_value:
            self.log_compliance_check('Position Value Limit', 'PASS', f"Position value: {position_value}, Limit: {max_position_value}")
            return True
        else:
            self.log_compliance_check('Position Value Limit', 'FAIL', f"Position value: {position_value}, Limit: {max_position_value}")
            return False

    def check_margin_requirement(self, account_equity, required_margin):
        """
        Check if the account equity meets the required margin.

        :param account_equity: The equity of the trading account
        :param required_margin: The required margin
        :return: Boolean indicating compliance status
        """
        if account_equity >= required_margin:
            self.log_compliance_check('Margin Requirement', 'PASS', f"Account equity: {account_equity}, Required margin: {required_margin}")
            return True
        else:
            self.log_compliance_check('Margin Requirement', 'FAIL', f"Account equity: {account_equity}, Required margin: {required_margin}")
            return False

    def check_regulatory_capital(self, capital, minimum_capital):
        """
        Check if the capital meets the regulatory minimum capital requirement.

        :param capital: The capital of the trading firm
        :param minimum_capital: The regulatory minimum capital requirement
        :return: Boolean indicating compliance status
        """
        if capital >= minimum_capital:
            self.log_compliance_check('Regulatory Capital Requirement', 'PASS', f"Capital: {capital}, Minimum capital: {minimum_capital}")
            return True
        else:
            self.log_compliance_check('Regulatory Capital Requirement', 'FAIL', f"Capital: {capital}, Minimum capital: {minimum_capital}")
            return False

    def get_compliance_log(self):
        """
        Get the compliance log.

        :return: List of compliance log entries
        """
        return self.compliance_log

# Example usage:
if __name__ == "__main__":
    compliance = RegulatoryCompliance()
    
    # Example compliance checks
    compliance.check_trade_limit(trade_volume=500, max_trade_volume=1000)
    compliance.check_position_limit(position_value=200000, max_position_value=250000)
    compliance.check_margin_requirement(account_equity=150000, required_margin=100000)
    compliance.check_regulatory_capital(capital=500000, minimum_capital=300000)
    
    # Print the compliance log
    compliance_log = compliance.get_compliance_log()
    for entry in compliance_log:
        print(entry)
