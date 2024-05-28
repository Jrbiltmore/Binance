import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskLimitsAlerts:
    def __init__(self, risk_limits):
        """
        Initialize the RiskLimitsAlerts with risk limits.

        :param risk_limits: Dictionary with risk limits for each risk factor
        """
        self.risk_limits = risk_limits
        self.alerts = []
        logger.info("RiskLimitsAlerts initialized with risk limits")

    def log_alert(self, risk_factor, value, limit, message):
        """
        Log an alert for a risk limit breach.

        :param risk_factor: The risk factor that breached the limit
        :param value: The value that caused the breach
        :param limit: The predefined risk limit
        :param message: The alert message
        """
        alert = {
            'timestamp': datetime.now(),
            'risk_factor': risk_factor,
            'value': value,
            'limit': limit,
            'message': message
        }
        self.alerts.append(alert)
        logger.warning(f"Risk limit alert: {alert}")

    def check_risk_limits(self, risk_factors):
        """
        Check the current values of risk factors against predefined risk limits.

        :param risk_factors: Dictionary with current values of risk factors
        :return: List of alerts for any breaches
        """
        alerts = []
        for risk_factor, value in risk_factors.items():
            if risk_factor in self.risk_limits:
                limit = self.risk_limits[risk_factor]
                if value > limit:
                    message = f"Risk limit breached for {risk_factor}: {value} exceeds limit of {limit}"
                    self.log_alert(risk_factor, value, limit, message)
                    alerts.append(message)
                else:
                    logger.info(f"Risk factor {risk_factor} is within the limit: {value} <= {limit}")
        return alerts

    def get_alerts(self):
        """
        Get the list of alerts.

        :return: List of alert entries
        """
        return self.alerts

# Example usage:
if __name__ == "__main__":
    # Example risk limits
    risk_limits = {
        'VaR': 100000,  # Value at Risk limit
        'Position Size': 500000,  # Position size limit
        'Leverage': 10  # Leverage limit
    }

    # Example current risk factor values
    current_risk_factors = {
        'VaR': 120000,
        'Position Size': 450000,
        'Leverage': 12
    }

    risk_alerts = RiskLimitsAlerts(risk_limits)
    alerts = risk_alerts.check_risk_limits(current_risk_factors)
    
    if alerts:
        print("Risk limit alerts:")
        for alert in alerts:
            print(alert)
    else:
        print("No risk limit breaches detected.")

    # Print all logged alerts
    all_alerts = risk_alerts.get_alerts()
    print("All logged alerts:")
    for alert in all_alerts:
        print(alert)
