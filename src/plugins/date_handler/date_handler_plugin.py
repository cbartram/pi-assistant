from datetime import datetime
from src.plugins.plugin import Plugin
from src.pi_assistant import assistant_reply
from src.plugins.plugin_configuration import PluginConfiguration


class DateHandlerPlugin(Plugin):
    """
    This plugin tells the user the current month and day of the month.
    """
    def name(self):
        return "date_handler"

    def bind_to(self) -> str:
        return "date"

    def init(self, config: PluginConfiguration = None) -> None:
        pass

    def on_intent_received(self, intent: dict) -> None:
        now = datetime.now()
        suffix = 'th' if 11 <= now.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(now.day % 10, 'th')
        assistant_reply("The current date_helper is " + now.strftime("%B {S}").replace('{S}', str(now.day) + suffix))

    def on_plugin_end(self) -> None:
        pass
