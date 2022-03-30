from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    Class which is inherited by every plugin and provides a unified way to implement IoT
    actions for a given intent.
    """

    @abstractmethod
    def bind_to(self) -> str:
        """
        Determines the intent to which the given plugin will be bound to. For example if the plugin is for Smart home
        lighting it should return a string "smart_lights" which will match the intent defined in Wit.ai. This tells
        the system that whenever the smart_lights intent is observed for an utterance this logic should execute.

        :return: String the name of the wi
        """

