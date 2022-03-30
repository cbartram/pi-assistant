import os


class WeatherConfig:

    def open_weather_api_key(self):
        return os.getenv("OPEN_WEATHER_API_KEY", "OPEN_WEATHER_DEFAULT_API_KEY")
