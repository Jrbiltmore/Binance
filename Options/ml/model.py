import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingModel:
    def __init__(self, model=None):
        """
        Initialize the TradingModel class.

        :param model: An instance of a scikit-learn estimator (optional)
        """
        self.model = model if model else RandomForestClassifier()
        logger.info("TradingModel initialized with model: %s", self.model.__class__.__name__)

    def prepare_data(self, data, target_column, test_size=0.2, random_state=42):
        """
        Prepare data for training and evaluation.

        :param data: DataFrame containing the features and target column
        :param target_column: Name of the target column
        :param test_size: Proportion of the dataset to include in the test split
        :param random_state: Seed used by the random number generator
        :return: Tuple of (X_train, X_test, y_train, y_test)
        """
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        logger.info("Data prepared with test size: %s", test_size)
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train, param_grid=None, cv=5):
        """
        Train the model using the provided training data.

        :param X_train: Training features
        :param y_train: Training target
        :param param_grid: Dictionary with parameters names as keys and lists of parameter settings to try as values (optional)
        :param cv: Number of folds in cross-validation
        :return: Trained model
        """
        if param_grid:
            logger.info("Performing grid search with parameters: %s", param_grid)
            grid_search = GridSearchCV(self.model, param_grid, cv=cv, n_jobs=-1)
            grid_search.fit(X_train, y_train)
            self.model = grid_search.best_estimator_
            logger.info("Best parameters found: %s", grid_search.best_params_)
        else:
            self.model.fit(X_train, y_train)
            logger.info("Model trained without hyperparameter tuning")
        return self.model

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model using the provided test data.

        :param X_test: Test features
        :param y_test: Test target
        :return: Dictionary with evaluation metrics
        """
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        logger.info("Model evaluation completed with accuracy: %s", accuracy)
        logger.info("Classification report:\n%s", report)
        return {"accuracy": accuracy, "classification_report": report}

    def save_model(self, file_path):
        """
        Save the trained model to a file.

        :param file_path: Path to the file where the model will be saved
        """
        joblib.dump(self.model, file_path)
        logger.info("Model saved to file: %s", file_path)

    def load_model(self, file_path):
        """
        Load a trained model from a file.

        :param file_path: Path to the file where the model is saved
        :return: Loaded model
        """
        self.model = joblib.load(file_path)
        logger.info("Model loaded from file: %s", file_path)
        return self.model

# Example usage:
if __name__ == "__main__":
    # Example data
    data = pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'target': np.random.choice([0, 1], size=100)
    })

    model = TradingModel()
    X_train, X_test, y_train, y_test = model.prepare_data(data, 'target')
    param_grid = {'n_estimators': [100, 200], 'max_depth': [3, 5, 10]}
    model.train(X_train, y_train, param_grid)
    evaluation_metrics = model.evaluate(X_test, y_test)
    model.save_model('trading_model.pkl')
    loaded_model = model.load_model('trading_model.pkl')
