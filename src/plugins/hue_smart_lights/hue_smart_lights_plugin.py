from src.plugins.plugin import Plugin


class HueSmartLightsPlugin(Plugin):
    def bind_to(self) -> str:
        return "hue_smart_lights"

    def init(self) -> None:
        pass

    def on_intent_received(self, intent: dict) -> None:
        pass

    def on_plugin_end(self) -> None:
        pass