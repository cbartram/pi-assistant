from pi_assistant.plugins.plugin import Plugin
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class HueSmartLightsPlugin(Plugin):
    def bind_to(self) -> str:
        return "hue_smart_lights"

    def name(self):
        return "hue_smart_lights"

    def init(self, config: PluginConfiguration = None) -> None:
        pass

    def on_intent_received(self, intent: dict) -> None:
        pass

    def on_plugin_end(self) -> None:
        pass
