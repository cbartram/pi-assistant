from src.plugins.plugin import Plugin


class DatePlugin(Plugin):
    def bind_to(self) -> str:
        return "date"

    def init(self) -> None:
        pass

    def on_intent_received(self) -> None:
        pass

    def on_plugin_end(self) -> None:
        pass
