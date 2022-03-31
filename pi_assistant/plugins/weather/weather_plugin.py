import requests
from pi_assistant.log import logger
from pi_assistant.plugins.plugin import Plugin
from pi_assistant.main import assistant_reply
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class WeatherPlugin(Plugin):
    def __init__(self):
        self._config = None
        self._current_city = None
        self._current_state = None
        self._current_temperature_f = None  # Temperature in farenheight
        self._feels_like_temperature_f = None
        self._forecast = None  # Cloudy, Rainy, Sunny

    def name(self):
        return "weather"

    def bind_to(self) -> str:
        return "wit$get_weather"

    def init(self, config: PluginConfiguration = None) -> None:
        self._config = config
        location_response = requests.get('https://ipinfo.io').json()
        logger.debug(f"IP Location info response: {location_response}")
        self._current_city = location_response['city']
        self._current_state = location_response['region']

        weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={self._current_city},{self._current_state}&APPID={self._config.open_weather_api_key()}').json()
        logger.debug(f"Weather map response: {weather_response}")
        self._forecast = weather_response['weather'][0]['main'] # TODO need more error checking in these requests and here
        self._current_temperature_f = weather_response['main']['temp']
        self._feels_like_temperature_f = weather_response['main']['feels_like']

    def on_intent_received(self, intent: dict) -> None:
        # TODO how often should we re-fetch weather? Implement that logic somewhere so the cache in init() doesn't go stale
        # maybe if feels_like > or < 20º difference from temp include it in the assistant response else exclude it since user didn't ask for it
        assistant_reply(f"It is currently {self._forecast} in {self._current_city} {self._current_state}. The temperature is {self._current_temperature_f} and it feels like {self._feels_like_temperature_f}")

    def on_plugin_end(self) -> None:
        pass
