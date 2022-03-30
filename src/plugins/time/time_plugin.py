from src.plugins.plugin import Plugin


class TimePlugin(Plugin):
    def bind_to(self) -> str:
        return "time"

    def init(self) -> None:
        pass

    def on_intent_received(self) -> None:
        pass

    def on_plugin_end(self) -> None:
        pass
