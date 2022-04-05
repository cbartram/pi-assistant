import os
import json
import tinytuya
from pi_assistant.log import logger
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class FeitElectricSmartLightsConfig(PluginConfiguration):

    def __init__(self):
        self._devices = []

        # Attempt to load cached device data from a local json file if it exists. Scanning for devices on
        # the network takes a really long time
        devices_file_path = os.path.join(".", "pi_assistant", "plugins", "feit_electric_smart_lights", "devices.json")
        if os.path.exists(devices_file_path):
            logger.info("Loading existing Feit devices from cached json file.")
            with open(devices_file_path, 'r') as devices_json:
                devices = json.loads(devices_json.read())
                self._devices = FeitElectricSmartLightsConfig.parse_device_data(devices)
        else:
            logger.info("Scanning for Feit electric devices on the local network...")
            devices = tinytuya.deviceScan()
            reformatted_devices = FeitElectricSmartLightsConfig.parse_device_data(devices)
            # Write the reformatted devices to json file for fast load next time
            with open(devices_file_path, 'w') as file:
                file.write(json.dumps(devices))
                file.close()
            self._devices = reformatted_devices

    @staticmethod
    def parse_device_data(devices: dict) -> list:
        """
        Device data is nested in a json structure like: [ { <ip>: { ... }}, { <ip2>: {}}]
        This method unwraps the devices into a single list and throws away unnecessary information keeping only
        the security key, device id, name, and ip address.
        :param devices: List of devices from tinytuya network scan.
        :return: List
        """
        output = []
        for device_ip in devices.keys():
            device = devices[device_ip]
            output.append({
                'name': device['name'],
                'key': device['key'],
                'ip': device_ip,
                'id': device['gwId']
            })
        return output

    @property
    def devices(self):
        return self._devices
