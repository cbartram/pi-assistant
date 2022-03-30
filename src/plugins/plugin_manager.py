import os
import src.plugins.plugin
from src.log import logger
from src.config import Configuration
from src.util import sanitize_plugin_class_name


class PluginManager:
    """
    Acts as a way to load and provide references to each plugin
    """

    def __init__(self, config: Configuration = Configuration()):
        self._plugins = []
        self._configs = {}  # The configuration for each respective plugin
        self._initialized_plugins = []
        self._config = config

    def init_plugins(self):
        """
        Initializes each plugin class and calls the "init" method of each plugin
        :return:
        """
        self._plugins = PluginManager.load_plugins()
        self._configs = PluginManager.load_config()
        initialized_plugins = []
        for plugin in self._plugins:
            p = plugin()

            # IMPORTANT: Plugin's name() method must return the same string case-sensitive as the module for which
            # the plugin is enclosed. self._configs is keyed by the module's name NOT the plugin's name() method. If
            # these mis-match there will be an initialized plugin without any injected configuration
            if p.name() in self._configs:
                p.init(config=self._configs[p.name()]())
            initialized_plugins.append(p)

        self._initialized_plugins = initialized_plugins

    def get_bound_plugin_for(self, intent: str) -> src.plugins.plugin.Plugin:
        """
        Returns a plugin object which is bound to the respective Wit intent passed in as a parameter
        :param intent: String the wit intent to find a plugin for
        :return: Plugin object
        """
        if intent.lower() not in self._config.get("wit.intents"):
            raise KeyError(f'The intent specified: {intent} is not a known intent: {self._config.get("wit.intents")}')

        logger.info(f"Looking for plugin bound to intent: {intent}")
        for plugin in self._initialized_plugins:
            logger.info(f"Plugin: {plugin.__class__} is bound to: {plugin.bind_to()}",)
            if plugin.bind_to() == intent:
                return plugin
        return None

    def handle_intent(self, wit_response: dict) -> None:
        """
        Handles an intent by locating a plugin which matches the given intent and running the plugin.
        :param wit_response: Dictionary the response returned from the wit client.
        :return: None
        """
        if len(wit_response['intents']) == 0:
            raise Exception("Uncategorizable utterance did not match any intents.")

        sorted_intents = sorted(wit_response['intents'], key=lambda intent: intent['confidence'])
        for intent in sorted_intents:
            logger.info(f"Intent: {intent}")
            plugin = self.get_bound_plugin_for(intent['name'])
            try:
                plugin.on_intent_received(intent)
                plugin.on_plugin_end()
            except Exception as e:
                logger.error(f"Exception thrown while attempting to run the plugin: {plugin.__class__} with intent: {intent}. "
                             f"Error Message = {str(e)}")

    @staticmethod
    def load_plugins() -> list:
        """
        Loads all the valid plugins defined within the src.plugins module. The loaded plugins will be a class object
        which can be dynamically instantiated to create the actual plugin
        :return:
        """
        plugins = []
        path = os.path.join(".", "src", "plugins")
        plugin_names = list(filter(lambda directory: directory != '__pycache__', next(os.walk(path))[1]))
        for plugin_name in plugin_names:
            class_name = sanitize_plugin_class_name(plugin_name)
            mod = __import__(f'src.plugins.{plugin_name}.{plugin_name}_plugin', fromlist=[class_name])
            plugins.append(getattr(mod, class_name))
        logger.info(f"Successfully loaded: {len(plugins)} plugins.")
        return plugins

    @staticmethod
    def load_config() -> dict:
        """
        Loads all the configuration objects for the each plugin. If the plugin does not define a configuration class
        it is omitted.
        :return: dictionary of configuration classes keyed by the plugin name
        """
        configs = {}
        path = os.path.join(".", "src", "plugins")
        module_names = list(filter(lambda directory: directory != '__pycache__', next(os.walk(path))[1]))

        for module in module_names:
            config_class_name = sanitize_plugin_class_name(module, True)
            config_file_path = os.path.join(path, module, f"{module}_config.py")
            if os.path.exists(config_file_path):
                mod = __import__(f'src.plugins.{module}.{module}_config', fromlist=[config_class_name])
                configs[module] = getattr(mod, config_class_name)
            else:
                logger.debug(f"No configuration file found for plugin: {module} in path: {config_file_path}")
        logger.info(f"Successfully loaded: {len(configs.keys())} configuration modules.")
        logger.debug(f"Configuration object keys: {configs.keys()}")
        return configs

    @property
    def plugins(self) -> list:
        return self._plugins
