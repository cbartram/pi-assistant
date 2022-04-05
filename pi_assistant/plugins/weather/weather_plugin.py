import requests
from pi_assistant.log import logger
from pi_assistant.config import Configuration
from pi_assistant.util import assistant_reply
from pi_assistant.plugins.plugin import Plugin
from pi_assistant.plugins.plugin_configuration import PluginConfiguration


class WeatherPlugin(Plugin):
    """
    Uses the user's local position (city and region only) to determine
    the current weather forecast and temperature.
    """
    def enabled(self) -> bool:
        return bool(self._app_config.get("plugins.weather.enabled"))

    def bind_to(self) -> str:
        return "wit$get_weather"

    def init(self, config: PluginConfiguration = None) -> None:
        self._city = None
        self._region = None
        self._current_temperature_f = None  # Temperature in farenheight
        self._feels_like_temperature_f = None
        self._forecast = None  # Cloudy, Rainy, Sunny
        self._config = config
        self._city, self._region = self.get_location()
        self._forecast, self._current_temperature_f, self._feels_like_temperature_f = \
            self.get_weather_report(self._city, self._region)

    def on_intent_received(self, intent: dict, entities: dict) -> None:
        # TODO how often should we re-fetch weather? Implement that logic somewhere so the cache in init() doesn't go stale
        # maybe if feels_like > or < 20º difference from temp include it in the assistant response else exclude it since user didn't ask for it
        assistant_reply(f"It is currently {self._forecast} in {self._city} {self._region}. The temperature is {self._current_temperature_f} and it feels like {self._feels_like_temperature_f}")

    def on_plugin_end(self) -> None:
        pass

    def get_weather_report(self, city: str, region: str) -> tuple:
        """
        Fetches the current weather report given a city and region
        :param: city String the city to fetch the weather report for
        :param: state String the state to fetch teh weather report for
        :return:
        """
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{region}' \
              f'&APPID={self._config.open_weather_api_key()}'
        try:
            r = requests.get(url)
            if r.status_code == 200:
                weather_response = r.json()
                logger.debug(f"Weather map response: {weather_response}")
                # TODO need more checking of the response data here
                return weather_response['weather'][0]['main'], weather_response['main']['temp'], weather_response['main']['feels_like']
            else:
                logger.error(f"Expected 200 HTTP status code from Weather API but received status code of: "
                             f"{r.status_code}. Response = {r.content}")
                return "Unknown", "Unknown", "Unknown"
        except requests.exceptions.Timeout:
            # TODO Maybe set up for a retry, or continue in a retry loop
            logger.error(f"A timeout exception occurred while waiting for a response from: {url}.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Something went wrong while attempting to fetch data from: {url}. Error = {str(e)}")
            raise Exception(f"Something went wrong while attempting to fetch data from: {url}. Error = {str(e)}")

    def get_location(self) -> tuple:
        """
        Fetches the city and state the current user resides in.
        :return:
        """
        url = "https://ipinfo.io"
        try:
            r = requests.get(url)

            if r.status_code == 200:
                location_response = r.json()
                logger.debug(f"IP Location info response: {location_response}")
                return (location_response['city'], location_response['region'])
            else:
                logger.error(f"Expected 200 HTTP status code from Location API but received status code of: "
                             f"{r.status_code}. Response = {r.content}")
                # TODO maybe make the default city/state configurable
                return ("New York", "New York")
        except requests.exceptions.Timeout:
            # TODO Maybe set up for a retry, or continue in a retry loop
            logger.error(f"A timeout exception occurred while waiting for a response from: {url}.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Something went wrong while attempting to fetch data from: {url}. Error = {str(e)}")
            raise Exception(f"Something went wrong while attempting to fetch data from: {url}. Error = {str(e)}")

