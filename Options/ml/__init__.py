"""
Machine Learning Module for Binance Options Trading System

This module provides machine learning functionalities to enhance the trading strategies
and decision-making processes. It includes modules for data preprocessing, model training,
evaluation, and prediction.

Modules:
    - data_preprocessing: Preprocessing market data for machine learning models.
    - model_training: Training machine learning models for trading strategies.
    - model_evaluation: Evaluating the performance of machine learning models.
    - prediction: Making predictions using trained machine learning models.
"""

# Import necessary modules for machine learning functionalities
from .data_preprocessing import DataPreprocessing
from .model_training import ModelTraining
from .model_evaluation import ModelEvaluation
from .prediction import Prediction
