from unittest import mock
from pi_assistant.plugins.plugin_manager import PluginManager
from pi_assistant.plugins.date_handler.date_handler_plugin import DateHandlerPlugin
from pi_assistant.plugins.temporal_handler.temporal_handler_plugin import TemporalHandlerPlugin


def test_plugin_manager_loads_plugins_success():
    plugin_manger = PluginManager()
    plugins = plugin_manger.load_plugins()
    assert type(plugins) == list
    assert len(plugins) > 0


def test_plugin_manager_loads_plugin_config_success():
    plugin_manger = PluginManager()
    loaded_config = plugin_manger.load_config()
    assert type(loaded_config) == dict
    assert len(loaded_config.keys()) > 0


# Need to mock the init method of the weather plugin because it makes API calls
@mock.patch('pi_assistant.plugins.weather.weather_plugin.WeatherPlugin.init', side_effect=lambda config: config)
@mock.patch('pi_assistant.plugins.feit_electric_smart_lights.feit_electric_smart_lights_plugin.FeitElectricSmartLightsPlugin.enabled', side_effect=lambda: False)
def test_plugin_manager_init_initializes_plugins_success(mocked_init, mock_feit):
    plugin_manger = PluginManager()
    plugin_manger.init_plugins()
    assert type(plugin_manger._initialized_plugins) == list
    assert len(plugin_manger._initialized_plugins) > 0
    for plugin in plugin_manger._initialized_plugins:
        for base in plugin.__class__.__bases__:
            name = base.__name__
            assert name == 'Plugin'

    assert len(plugin_manger._initialized_plugins) == len(plugin_manger.plugins) - 2


@mock.patch('pi_assistant.plugins.weather.weather_plugin.WeatherPlugin.enabled', side_effect=lambda: False)
@mock.patch('pi_assistant.plugins.feit_electric_smart_lights.feit_electric_smart_lights_plugin.FeitElectricSmartLightsPlugin.enabled', side_effect=lambda: False)
def test_plugin_manager_init_initializes_plugins_skips_disabled_plugins(mocked_init, mock_feit):
    plugin_manger = PluginManager()
    total_plugins = len(plugin_manger.load_plugins())
    plugin_manger.init_plugins()
    assert len(plugin_manger._initialized_plugins) == (total_plugins - 2)


@mock.patch('pi_assistant.plugins.weather.weather_plugin.WeatherPlugin.init', side_effect=lambda config: config)
@mock.patch('pi_assistant.plugins.feit_electric_smart_lights.feit_electric_smart_lights_plugin.FeitElectricSmartLightsPlugin.enabled', side_effect=lambda: False)
def test_plugin_manager_gets_bound_plugin_for_intent(mocked_init, mock_feit):
    plugin_manger = PluginManager()
    plugin_manger.init_plugins()
    assert len(plugin_manger._initialized_plugins) == len(plugin_manger.plugins) - 2

    time_plugin = plugin_manger.get_bound_plugin_for("time")
    date_plugin = plugin_manger.get_bound_plugin_for("date")

    assert type(time_plugin) == TemporalHandlerPlugin
    assert type(date_plugin) == DateHandlerPlugin


def test_plugin_manager_gets_bound_plugin_for_throws_error_invalid_intent():
    plugin_manger = PluginManager()
    assert len(plugin_manger._initialized_plugins) == len(plugin_manger.plugins)
    try:
        plugin_manger.get_bound_plugin_for("not_a_real_wit_intent")
    except KeyError as e:
        assert "The intent specified: not_a_real_wit_intent is not a known intent:" in str(e)


# Must mock the assistant reply function so that it doesn't inadvertently speak a reply during tests
@mock.patch('pi_assistant.main.assistant_reply', side_effect=lambda text: text)
@mock.patch('pi_assistant.plugins.weather.weather_plugin.WeatherPlugin.init', side_effect=lambda config: config)
@mock.patch('pi_assistant.plugins.feit_electric_smart_lights.feit_electric_smart_lights_plugin.FeitElectricSmartLightsPlugin.enabled', side_effect=lambda: False)
def test_plugin_manager_handle_intent_success(side_effect, assistant_reply, mock_feit):
    plugin_manger = PluginManager()
    plugin_manger.init_plugins()

    intents = {
        'intents': [
            # It will execute the time intent because it has the highest confidence
            {'id': '5013819665334140', 'name': 'time', 'confidence': 0.9933},
            {'id': '5013819665334140', 'name': 'date', 'confidence': 0.9831}
        ],
        'entities': []
    }

    plugin = plugin_manger.handle_intent(intents)
    assert type(plugin) == TemporalHandlerPlugin


@mock.patch('pi_assistant.plugins.weather.weather_plugin.WeatherPlugin.init', side_effect=lambda config: config)
@mock.patch('pi_assistant.plugins.feit_electric_smart_lights.feit_electric_smart_lights_plugin.FeitElectricSmartLightsPlugin.enabled', side_effect=lambda: False)
def test_plugin_manager_handle_intent_no_intents_error(side_effect, mock_feit):
    plugin_manger = PluginManager()
    plugin_manger.init_plugins()

    intents = {
        'intents': []  # No intents cause an error
    }

    try:
        plugin_manger.handle_intent(intents)
    except Exception as e:
        assert "Uncategorizable utterance did not match any intents." in str(e)

