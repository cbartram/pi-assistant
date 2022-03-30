from src.plugins.plugin_manager import PluginManager


def test_plugin_manager_loads_plugins_success():
    plugin_manger = PluginManager()
    plugin_manger.load_plugins()
    assert 1 == 2

