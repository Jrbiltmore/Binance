"""
Data Module for Binance Options Trading System

This module provides functionalities for data management within the Binance Options trading system.
It includes modules for fetching, storing, and processing market and trade data.

Modules:
    - data_fetcher: Fetching market data from Binance API.
    - data_processor: Processing and analyzing market data.
    - database: Handling database operations for storing trade and market data.
"""

# Import necessary modules for data management functionalities
from .data_fetcher import DataFetcher
from .data_processor import DataProcessor
from .database import Database
