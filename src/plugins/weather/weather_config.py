import os
from src.plugins.plugin_configuration import PluginConfiguration


class WeatherConfig(PluginConfiguration):

    def open_weather_api_key(self):
        return os.getenv("OPEN_WEATHER_API_KEY", "OPEN_WEATHER_DEFAULT_API_KEY")
