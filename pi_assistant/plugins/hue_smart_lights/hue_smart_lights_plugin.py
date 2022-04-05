from pi_assistant.plugins.plugin import Plugin
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class HueSmartLightsPlugin(Plugin):
    def enabled(self) -> bool:
        return bool(self._app_config.get("plugins.hue_smart_lights.enabled"))

    def get_devices(self) -> list:
        return []

    def bind_to(self) -> str:
        return "hue_smart_lights"

    def init(self, config: PluginConfiguration = None) -> None:
        pass

    def on_intent_received(self, intent: dict, entities: dict) -> None:
        pass

    def on_plugin_end(self) -> None:
        pass
