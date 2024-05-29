"""
Trading module for Binance Options.

This module contains various classes and functions to facilitate trading
operations, risk management, strategy implementation, and transaction cost analysis
for Binance Options trading.

Modules:
    - algo_risk_management: Algorithmic risk management for trading strategies.
    - algorithmic_throttling: Implementing throttling mechanisms for trading algorithms.
    - beta_hedging: Implementing beta hedging strategies.
    - counterparty_risk: Managing counterparty risk.
    - credit_risk: Managing credit risk.
    - cvar: Calculating Conditional Value at Risk (CVaR).
    - data_fetcher: Fetching market data and options data from Binance API.
    - data_processor: Processing and analyzing market data.
    - database: Handling database operations for trade and market data.
    - diversification: Implementing diversification strategies.
    - drawdown_control: Managing drawdown control strategies.
    - dynamic_hedging: Implementing dynamic hedging strategies.
    - esg_risk: Managing ESG (Environmental, Social, and Governance) risk.
    - execution: Executing trades and managing orders.
    - factor_exposure: Analyzing factor exposure.
    - hft_risk_controls: Implementing risk controls for high-frequency trading.
    - liquidity_risk: Managing liquidity risk.
    - market_sentiment_analysis: Analyzing market sentiment.
    - position_sizing: Calculating position sizes based on risk management rules.
    - portfolio_rebalancing: Rebalancing the trading portfolio.
    - regulatory_compliance: Ensuring regulatory compliance.
    - risk_limits_alerts: Setting risk limits and generating alerts.
    - risk_overlay: Applying risk overlay to the portfolio.
    - scenario_analysis: Performing scenario analysis on the portfolio.
    - sharpe_ratio_optimization: Optimizing portfolio based on Sharpe ratio.
    - statistical_arbitrage: Implementing statistical arbitrage strategies.
    - stop_loss: Managing stop-loss strategies for trades.
    - stress_testing: Performing stress testing on the portfolio.
    - transaction_cost_analysis: Analyzing transaction costs and their impact on trades.
    - var: Calculating Value at Risk (VaR) for the portfolio.
"""

# Expose the key classes and functions in the module
from .algo_risk_management import AlgorithmicRiskManagement
from .algorithmic_throttling import AlgorithmicThrottling
from .beta_hedging import BetaHedging
from .counterparty_risk import CounterpartyRisk
from .credit_risk import CreditRisk
from .cvar import ConditionalValueAtRisk
from .data_fetcher import DataFetcher
from .data_processor import DataProcessor
from .database import Database
from .diversification import Diversification
from .drawdown_control import DrawdownControl
from .dynamic_hedging import DynamicHedging
from .esg_risk import ESGRisk
from .execution import Execution
from .factor_exposure import FactorExposure
from .hft_risk_controls import HFTRiskControls
from .liquidity_risk import LiquidityRisk
from .market_sentiment_analysis import MarketSentimentAnalysis
from .position_sizing import PositionSizing
from .portfolio_rebalancing import PortfolioRebalancing
from .regulatory_compliance import RegulatoryCompliance
from .risk_limits_alerts import RiskLimitsAlerts
from .risk_overlay import RiskOverlay
from .scenario_analysis import ScenarioAnalysis
from .sharpe_ratio_optimization import SharpeRatioOptimization
from .statistical_arbitrage import StatisticalArbitrage
from .stop_loss import StopLoss
from .stress_testing import StressTesting
from .transaction_cost_analysis import TransactionCostAnalysis
from .var import ValueAtRisk
