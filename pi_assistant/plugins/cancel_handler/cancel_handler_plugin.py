from pi_assistant.plugins.plugin import Plugin
from pi_assistant.main import assistant_reply
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class CancelHandlerPlugin(Plugin):
    """
    A default plugin which executes when no intents are known or if the user cancels a command by saying
    something like: "nevermind", "stop", or "goodbye"
    """
    def name(self):
        return "cancel_handler"

    def bind_to(self) -> str:
        return "wit$cancel"

    def init(self, config: PluginConfiguration = None) -> None:
        pass

    def on_intent_received(self, intent: dict) -> None:
        assistant_reply("Okay I will be here if you need anything.")

    def on_plugin_end(self) -> None:
        pass
