import tinytuya
from pi_assistant.plugins.plugin_configuration import PluginConfiguration

class FeitElectricSmartLightsConfig(PluginConfiguration):

    def __init__(self):
        devices = tinytuya.deviceScan()
        self._devices = devices

    @property
    def devices(self):
        return self._devices