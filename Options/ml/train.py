import pandas as pd
import numpy as np
import logging
from model import TradingModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data(file_path):
    """
    Load data from a CSV file.

    :param file_path: Path to the CSV file
    :return: DataFrame containing the loaded data
    """
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Data loaded from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise

def main():
    # Load the data
    data_file_path = 'trading_data.csv'  # Update with the correct path
    data = load_data(data_file_path)

    # Initialize the model
    model = TradingModel()

    # Prepare the data
    target_column = 'target'  # Update with the correct target column
    X_train, X_test, y_train, y_test = model.prepare_data(data, target_column)

    # Train the model with hyperparameter tuning
    param_grid = {'n_estimators': [100, 200], 'max_depth': [3, 5, 10]}
    model.train(X_train, y_train, param_grid)

    # Evaluate the model
    evaluation_metrics = model.evaluate(X_test, y_test)
    logger.info(f"Evaluation Metrics: {evaluation_metrics}")

    # Save the trained model
    model_file_path = 'trained_trading_model.pkl'  # Update with the correct path
    model.save_model(model_file_path)

if __name__ == "__main__":
    main()
