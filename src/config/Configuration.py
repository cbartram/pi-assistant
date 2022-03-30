import os
import yaml

class Configuration:

    def __init__(self, environment: str = os.getenv("ENVIRONMENT", "LOCAL")):
        self._environment = environment
        # Always load application.yml as the default configuration but if additional env specific
        # configuration is present it should overwrite values specified in application.yml
        with open('resources/application.yml', 'r') as file:
            self._yaml_config = yaml.safe_load(file)
        print(self._yaml_config)

    def get(self, key: str) -> str:
        pass

    def get_environment(self):
        return self._environment



