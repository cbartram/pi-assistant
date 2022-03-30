import requests
from src.plugins.plugin import Plugin
from src.plugins.plugin_configuration import PluginConfiguration


class WeatherPlugin(Plugin):
    def __init__(self):
        self._config = None
        self._current_city = None
        self._current_state = None
        self._current_temperature_f = None # Temperature in farenheight
        self._forecast = None # Cloudy, Rainy, Sunny


    def bind_to(self) -> str:
        return "weather"

    def init(self, config: PluginConfiguration = None) -> None:
        self._config = config
        location_response = requests.get('https://ipinfo.io').json()
        self._current_city = location_response['city']
        self._current_state = location_response['state']

        r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={self._current_city},{self._current_state}&APPID={APIKEY}')
        pass

    def on_intent_received(self, intent: dict) -> None:
        pass

    def on_plugin_end(self) -> None:
        pass
