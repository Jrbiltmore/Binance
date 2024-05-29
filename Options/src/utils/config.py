import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    def __init__(self, config_file):
        """
        Initialize the Config class with the path to the configuration file.

        :param config_file: Path to the JSON configuration file
        """
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        """
        Load configuration from a JSON file.

        :return: Dictionary containing configuration data
        """
        try:
            with open(self.config_file, 'r') as file:
                config_data = json.load(file)
                logger.info(f"Configuration loaded successfully from {self.config_file}")
                return config_data
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

    def get(self, key, default=None):
        """
        Get a configuration value by key.

        :param key: Key for the configuration value
        :param default: Default value if the key is not found
        :return: Configuration value
        """
        return self.config_data.get(key, default)

    def set(self, key, value):
        """
        Set a configuration value by key.

        :param key: Key for the configuration value
        :param value: Value to be set
        """
        self.config_data[key] = value
        self.save_config()
        logger.info(f"Set configuration key '{key}' to '{value}'")

    def save_config(self):
        """
        Save the current configuration to the JSON file.
        """
        try:
            with open(self.config_file, 'w') as file:
                json.dump(self.config_data, file, indent=4)
                logger.info(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            raise

# Example usage:
if __name__ == "__main__":
    config = Config('config.json')
    print(config.get('api_key'))
    config.set('api_key', 'new_api_key_value')
    print(config.get('api_key'))
