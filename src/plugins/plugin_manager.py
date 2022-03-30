import os
from src.util import sanitize_plugin_class_name


class PluginManager:
    """
    Acts as a way to load and provide references to each plugin
    """

    def __init__(self):
        self._plugins = PluginManager.load_plugins()


    def init_plugins(self):
        """
        Initializes each plugin class and calls the "init" method of each plugin
        :return:
        """
        for plugin in self._plugins:
            plugin().init()

    @staticmethod
    def load_plugins() -> list:
        """
        Loads all the valid plugins defined within the src.plugins module. The loaded plugins will be a class object
        which can be dynamically instantiated to create the actual plugin
        :return:
        """
        plugins = []
        path = os.path.join(".", "src", "plugins")
        plugin_names = list(filter(lambda directory: directory != '__pycache__', next(os.walk(path))[1]))
        for plugin_name in plugin_names:
            class_name = sanitize_plugin_class_name(plugin_name)
            mod = __import__(f'src.plugins.{plugin_name}.{plugin_name}_plugin', fromlist=[class_name])
            plugins.append(getattr(mod, class_name))
        return plugins

    @property
    def plugins(self) -> list:
        return self._plugins
