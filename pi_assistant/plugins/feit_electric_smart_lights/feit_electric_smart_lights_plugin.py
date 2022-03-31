import tinytuya
from pi_assistant.plugins.plugin import Plugin
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class FeitElectricSmartLightsPlugin(Plugin):

    def bind_to(self) -> str:
        return "feit_smart_lights"

    def init(self, config: PluginConfiguration = None) -> None:

        print(config.devices)

        # d = tinytuya.OutletDevice('DEVICE_ID_HERE', 'IP_ADDRESS_HERE', 'LOCAL_KEY_HERE')
        # d.set_version(3.3)
        # data = d.status()
        # print('set_status() result %r' % data)

    def on_intent_received(self, intent: dict) -> None:
        pass

    def on_plugin_end(self) -> None:
        pass