from datetime import datetime
from pi_assistant.main import assistant_reply
from pi_assistant.plugins.plugin import Plugin
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class TemporalHandlerPlugin(Plugin):
    """
    This plugin tells the user the current time in their timezone.
    """
    def enabled(self) -> bool:
        return bool(self._app_config.get("plugins.time.enabled"))

    def bind_to(self) -> str:
        return "time"

    def init(self, config: PluginConfiguration = None) -> None:
        pass

    def on_intent_received(self, intent: dict, entities: dict) -> None:
        assistant_reply("The current time is " + datetime.now().strftime("%I:%M %p"))

    def on_plugin_end(self) -> None:
        pass
