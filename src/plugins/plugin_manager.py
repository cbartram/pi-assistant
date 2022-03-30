import os

import src.plugins.plugin
from src.config import Configuration
from src.util import sanitize_plugin_class_name


class PluginManager:
    """
    Acts as a way to load and provide references to each plugin
    """

    def __init__(self, config: Configuration = Configuration()):
        self._plugins = PluginManager.load_plugins()
        self._initialized_plugins = []
        self._config = config

    def init_plugins(self):
        """
        Initializes each plugin class and calls the "init" method of each plugin
        :return:
        """
        initialized_plugins = []
        for plugin in self._plugins:
            p = plugin()
            p.init()
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

        for plugin in self._initialized_plugins:
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
            plugin = self.get_bound_plugin_for(intent['name'])
            plugin.on_intent_received(intent)
            plugin.on_plugin_end()

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
        return plugins

    @property
    def plugins(self) -> list:
        return self._plugins
