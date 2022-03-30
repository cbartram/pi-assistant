import os
import yaml
from src.log import logger


class Configuration:
    """
    Loads and provides an access point to a single source of application configuration
    """

    def __init__(self, environment: str = os.getenv("ENVIRONMENT", "LOCAL")):
        self._environment = environment
        # Always load application.yml as the default configuration but if additional env specific
        # configuration is present it should overwrite values specified in application.yml
        try:
            print()
            with open(os.path.join('.', 'resources', 'application.yml'), 'r') as file:
                self._yaml_config = yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Exception thrown while attempting to load application.yaml configuration properties. Error = {str(e)}")
            self._yaml_config = {}

        # Attempt to load any environment specific configuration
        path = os.path.join('resources', f'application-{environment.lower()}.yml')
        if os.path.exists(path):
            try:
                with open(path, 'r') as file:
                    # Merge two configuration files overwriting values from the environment specific config
                    self._yaml_config.update(yaml.safe_load(file))
            except Exception as e:
                logger.error(f"Exception thrown while attempting to load {path} configuration properties. Error = {str(e)}")

        else:
            logger.debug(f"No environment specific configuration exists for the environment: {environment.lower()}")

    def get(self, key: str) -> str:
        if key.endswith("."):
            raise KeyError("The key cannot end with a \".\"")

        if self._yaml_config is None or self._yaml_config is {}:
            raise Exception(f"Cannot retrieve configuration from null config. Using key: {key}")

        parts = key.split(".")
        data = None
        for k in parts:
            if data is None:
                if k in self._yaml_config:
                    data = self._yaml_config[k]
                else:
                    raise KeyError(f"The key part: {k} from the given key: {key} does not exist in the configuration. Config = {self._yaml_config}")
            else:
                if k in data:
                    data = data[k]
                else:
                    raise KeyError(f"The key part: {k} from the given key: {key} does not exist in the configuration. Config = {data}")
        return data

    def get_environment(self):
        return self._environment


