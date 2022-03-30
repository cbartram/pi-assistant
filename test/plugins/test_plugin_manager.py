from src.plugins.plugin_manager import PluginManager


def test_plugin_manager_loads_plugins_success():
    plugin_manger = PluginManager()
    plugin_manger.load_plugins()
    assert type(plugin_manger.plugins) == list
    assert len(plugin_manger.plugins) > 0

