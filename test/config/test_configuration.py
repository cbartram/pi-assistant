import pytest
from src.config import Configuration


def test_configuration_load_application_default_values_correctly():
    config = Configuration(environment="prod")
    assert config._yaml_config['voice_assistant'] is not None
    assert len(config._yaml_config['voice_assistant']['keywords']) == 3


def test_configuration_load_application_merges_values_correctly():
    config = Configuration(environment="local")
    assert config._yaml_config['voice_assistant'] is not None
    assert len(config._yaml_config['voice_assistant']['keywords']) == 1


def test_configuration_get_environment():
    config = Configuration(environment="local")
    assert config.get_environment() == "local"


def test_configuration_get_key():
    config = Configuration(environment="prod")
    keywords = config.get("voice_assistant.keywords")
    assert len(keywords) == 3
    assert keywords[0]['text'] == 'hey google'


def test_configuration_get_throws_error_on_invalid_key():
    try:
        config = Configuration(environment="prod")
        config.get("voice_assistant.invalid_key.")
    except Exception as e:
        assert "The key cannot end with a" in str(e)


def test_configuration_get_throws_error_on_failure_to_load_yaml():
    try:
        config = Configuration(environment="prod")
        config._yaml_config = None
        config.get("voice_assistant.keywords")
    except Exception as e:
        assert str(e) == "Cannot retrieve configuration from null config. Using key: voice_assistant.keywords"

@pytest.mark.parametrize("test_input,expected", [("voice_assistant.non_existent",
                                                  "The key part: non_existent from the given key: voice_assistant.non_existent does not exist in the configuration."),
                                                 ("bad_initial_key.keywords",
                                                  "The key part: bad_initial_key from the given key: bad_initial_key.keywords does not exist in the configuration.")])
def test_configuration_get_throws_error_on_non_existent_key(test_input, expected):
    try:
        config = Configuration(environment="prod")
        config.get(test_input)
    except Exception as e:
        assert "The key part:" in str(e)