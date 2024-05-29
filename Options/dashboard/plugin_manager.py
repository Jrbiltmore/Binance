import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self):
        """
        Initialize the PluginManager to manage dashboard plugins.
        """
        self.plugins = {}
        logger.info("PluginManager initialized")

    def load_plugin(self, name, plugin):
        """
        Load a plugin into the dashboard.

        :param name: Name of the plugin
        :param plugin: Plugin instance
        """
        self.plugins[name] = plugin
        logger.info(f"Loaded plugin: {name}")

    def get_plugin(self, name):
        """
        Retrieve a loaded plugin by name.

        :param name: Name of the plugin
        :return: Plugin instance
        """
        plugin = self.plugins.get(name)
        if plugin:
            logger.info(f"Retrieved plugin: {name}")
        else:
            logger.warning(f"Plugin not found: {name}")
        return plugin

    def unload_plugin(self, name):
        """
        Unload a plugin from the dashboard.

        :param name: Name of the plugin
        """
        if name in self.plugins:
            del self.plugins[name]
            logger.info(f"Unloaded plugin: {name}")
        else:
            logger.warning(f"Attempted to unload non-existent plugin: {name}")
