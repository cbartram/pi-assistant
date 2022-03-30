from src.plugins.plugin import Plugin


class WeatherPlugin(Plugin):
    def bind_to(self) -> str:
        return "weather"

    def init(self) -> None:
        pass

    def on_intent_received(self) -> None:
        pass