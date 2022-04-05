from abc import ABC, abstractmethod
from pi_assistant.config import Configuration
from pi_assistant.profile.Profile import Profile
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class Plugin(ABC):
    """
    Class which is inherited by every plugin and provides a unified way to implement IoT
    actions for a given intent.
    """
    def __init__(self, app_config: Configuration, profile: Profile):
        self._app_config = app_config
        self._profile = profile

    def name(self):
        """
        Defines a unique name for this plugin. This should be the same as the module (package) name this plugin
        is enclosed in. I.e for package: weather with weather_plugin.py the name should be "weather"
        :return:
        """
        return self.__module__.split(".")[-2]

    def get_devices(self) -> list:
        """
        Returns a list of available devices the extending plugin is able to interact with. The list will be of type:
        "Device" objects. Not all plugins interact with physical devices and as such this method is not abstract.
        Plugins do not have to implement this method unless they interact with IoT devices like light bulbs, plugs,
        vacuum cleaners, door locks, cameras etc...
        :return: List of device objects the plugin has access to.
        """
        return []

    def enabled(self) -> bool:
        """
        Determines if the plugin is enabled and should be used to respond to Wit.ai (user) intents. If this value
        is set to false the plugin will not be loaded and assistant functionality provided by the plugin will not be
        enabled. The default value for any plugin is true.
        :return: True if the plugin should be enabled and false otherwise.
        """
        return True

    @abstractmethod
    def bind_to(self) -> str:
        """
        Determines the intent to which the given plugin will be bound to. For example if the plugin is for Smart home
        lighting it should return a string "smart_lights" which will match the intent defined in Wit.ai. This tells
        the system that whenever the smart_lights intent is observed for an utterance this logic should execute.

        :return: String the name of the wit.ai intent to bind to
        """
        pass

    @abstractmethod
    def init(self, config: PluginConfiguration = None) -> None:
        """
        Executes when the plugin is first loaded and can be used to set initial variables or settings.
        :return:
        """
        pass

    @abstractmethod
    def on_intent_received(self, intent: dict, entities: dict) -> None:
        """
        Executes when a new intent is processed by Wit.ai and is ready for an IoT action to be take as a result.
        :return:
        """
        pass

    @abstractmethod
    def on_plugin_end(self) -> None:
        """
        Executes after the command has been process by this plugin and can close any open files or dispose of
        any outstanding resources.
        :return:
        """
