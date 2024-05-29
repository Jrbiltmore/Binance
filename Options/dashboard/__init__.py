"""
Dashboard Module for Binance Options Trading System

This module provides functionalities for the user interface and visualization within the Binance Options trading system.
It includes modules for creating and managing the trading dashboard, including portfolio management, watchlists,
real-time market data, and trading activity visualization.

Modules:
    - dashboard: Core functionalities for the trading dashboard.
    - portfolio_management: Managing the user's trading portfolio.
    - watchlist: Managing watchlists for tracking multiple trading symbols.
    - real_time_data: Fetching and displaying real-time market data.
    - trade_visualization: Visualizing trading activity and performance.
"""

# Import necessary modules for dashboard functionalities
from .dashboard import Dashboard
from .portfolio_management import PortfolioManagement
from .watchlist import Watchlist
from .real_time_data import RealTimeData
from .trade_visualization import TradeVisualization
