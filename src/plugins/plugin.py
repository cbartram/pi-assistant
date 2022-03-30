from src.plugins.plugin_configuration import PluginConfiguration
from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    Class which is inherited by every plugin and provides a unified way to implement IoT
    actions for a given intent.
    """

    @abstractmethod
    def name(self):
        """
        Defines a unique name for this plugin. This should be the same as the module (package) name this plugin
        is enclosed in. I.e for package: weather with weather_plugin.py the name should be "weather"
        :return:
        """
        pass

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
    def on_intent_received(self, intent: dict) -> None:
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
