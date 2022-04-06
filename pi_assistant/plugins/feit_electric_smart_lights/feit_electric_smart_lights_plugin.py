import tinytuya
from pi_assistant.log import logger
from pi_assistant.plugins.plugin import Plugin
from pi_assistant.plugins.plugin_configuration import PluginConfiguration
from pi_assistant.profile.Device import Device


class FeitElectricSmartLightsPlugin(Plugin):
    def enabled(self) -> bool:
        return bool(self._app_config.get("plugins.feit_electric_smart_lights.enabled"))

    def bind_to(self) -> str:
        return "smart_lights"

    def init(self, config: PluginConfiguration = None) -> None:
        self._lights = []
        self._config = config
        logger.info(f"Found {len(config.devices)} Feit bulbs on the network")
        for device in config.devices:
            light = tinytuya.BulbDevice(device['id'], device['ip'], device['key'])
            light.set_version(3.3)
            self._lights.append(light)

    def on_intent_received(self, intent: dict, entities: dict) -> None:
        light_state_value = entities['light_state:light_state'][0]['value']

        # TODO We need a notion of grouping items together so we can put the light_location entity into play here
        if light_state_value.lower() == "on":
            for light in self._lights:
                light.turn_on()
        else:
            for light in self._lights:
                light.turn_off()

    def get_devices(self) -> list:
        devices = []
        # This is always called after init() and thus it is safe to use init() set properties
        for device in self._config.devices:
            devices.append(Device(name=device['name'], bind_to=self.name(), metadata=device))
        return devices

    def on_plugin_end(self) -> None:
        pass