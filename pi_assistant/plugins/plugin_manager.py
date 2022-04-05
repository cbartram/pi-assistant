import os
import json
import pi_assistant.plugins.plugin
from pi_assistant.log import logger
from pi_assistant.config import Configuration
from pi_assistant.util import sanitize_plugin_class_name
from pi_assistant.profile.Profile import Profile


class PluginManager:
    """
    Acts as a way to load and provide references to each plugin
    """

    def __init__(self, config: Configuration = Configuration()):
        self._plugins = []
        self._configs = {}  # The configuration for each respective plugin
        self._initialized_plugins = []
        self._global_devices = []
        self._config = config

    def init_plugins(self, profile: Profile):
        """
        Initializes each plugin class and calls the "init" method of each plugin
        :return:
        """
        self._plugins = PluginManager.load_plugins()
        self._configs = PluginManager.load_config()  # Plugin level configuration i.e. weather_config.py
        initialized_plugins = []
        for plugin in self._plugins:
            try:
                p = plugin(self._config, profile)  # This self._config refers to application level config i.e. application.yml

                # IMPORTANT: Plugin's name() method must return the same string case-sensitive as the module for which
                # the plugin is enclosed. self._configs is keyed by the module's name NOT the plugin's name() method. If
                # these mismatch there will be an initialized plugin without any injected configuration
                if p.enabled():
                    if p.name() in self._configs:
                        p.init(config=self._configs[p.name()]())

                        # Some plugins interact with physical devices and the plugin manager needs to know about what
                        # devices the plugin interacts with. i.e Philips hue can interact with 1...N light bulbs while
                        # Roomba may simply interact with 1 vacuum cleaner. Users can use the CLI to link devices to
                        # specific rooms however, the plugin manager needs to maintain a global list of available
                        # devices to link.
                        if self._config.get(f"plugins.{p.name()}.physical_device") is True:
                            logger.info(f"The plugin has defined physical devices it uses: {p.name()}")
                            devices = p.get_devices()
                            logger.info(f"Found {len(devices)} IoT devices that the plugin: {p.name()} "
                                        f"is able to interact with.")
                            self._global_devices.append(devices)

                    initialized_plugins.append(p)
                else:
                    logger.info(f"The plugin: {p.name()} is disabled skipping initialization.")
            except Exception as e:
                logger.error(f"Exception thrown while attempting to initialize the plugins. Error = {str(e)}")
                raise e

        self.__save_devices()
        self._initialized_plugins = initialized_plugins

    def get_bound_plugin_for(self, intent: str) -> pi_assistant.plugins.plugin.Plugin:
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

    def handle_intent(self, wit_response: dict) -> pi_assistant.plugins.plugin.Plugin:
        """
        Handles an intent by locating a plugin which matches the given intent and running the plugin.
        :param wit_response: Dictionary the response returned from the wit client.
        :return: None
        """
        if len(wit_response['intents']) == 0:
            raise Exception("Uncategorizable utterance did not match any intents.")

        logger.info(f"Wit.ai Response: {wit_response}")
        sorted_intents = sorted(wit_response['intents'], key=lambda i: i['confidence'], reverse=True)
        for intent in sorted_intents:
            logger.info(f"Intent: {intent}")
            plugin = self.get_bound_plugin_for(intent['name'])
            try:
                plugin.on_intent_received(intent, wit_response['entities'])
                plugin.on_plugin_end()
                return plugin
            except Exception as e:
                logger.error(f"Exception thrown while attempting to run the plugin: {plugin.__class__} with intent: {intent}. "
                             f"Error Message = {str(e)}")
                raise e
                return None

    @staticmethod
    def load_plugins() -> list:
        """
        Loads all the valid plugins defined within the pi_assistant.plugins module. The loaded plugins will be a class object
        which can be dynamically instantiated to create the actual plugin
        :return:
        """
        plugins = []
        path = os.path.join(".", "pi_assistant", "plugins")
        plugin_names = list(filter(lambda directory: directory != '__pycache__', next(os.walk(path))[1]))
        for plugin_name in plugin_names:
            class_name = sanitize_plugin_class_name(plugin_name)
            mod = __import__(f'pi_assistant.plugins.{plugin_name}.{plugin_name}_plugin', fromlist=[class_name])
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
        path = os.path.join(".", "pi_assistant", "plugins")
        module_names = list(filter(lambda directory: directory != '__pycache__', next(os.walk(path))[1]))

        for module in module_names:
            config_class_name = sanitize_plugin_class_name(module, True)
            config_file_path = os.path.join(path, module, f"{module}_config.py")
            if os.path.exists(config_file_path):
                mod = __import__(f'pi_assistant.plugins.{module}.{module}_config', fromlist=[config_class_name])
                configs[module] = getattr(mod, config_class_name)
            else:
                logger.debug(f"No configuration file found for plugin: {module} in path: {config_file_path}")
        logger.info(f"Successfully loaded: {len(configs.keys())} configuration modules.")
        logger.debug(f"Configuration object keys: {configs.keys()}")
        return configs

    def __save_devices(self):
        """
        Saves all the plugin defined devices to a top level file in the resources directory
        :return:
        """
        path = os.path.join(".", "resources", "devices.json")
        try:
            with open(path, 'w') as devices_file:
                devices_file.write(json.dumps(self._global_devices, indent=4, default=lambda o: o.__dict__))
        except Exception as e:
            logger.error(f"Failed to save devices.json to path: {path}. Linking devices to rooms/groups will not work"
                         f"until this is resolved. Error = {str(e)}")

    @property
    def plugins(self) -> list:
        return self._plugins

    @property
    def configs(self):
        return self._configs

    @property
    def devices(self):
        return self._global_devices
