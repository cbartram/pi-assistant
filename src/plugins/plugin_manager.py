import os


class PluginManager:


    def load_plugins(self):
        print(os.path.abspath(os.path.join(".", "src", "plugins")))
        path = os.path.join(".", "src", "plugins")
        packages = next(os.walk(path))[1]
        print(packages)