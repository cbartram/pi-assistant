from pi_assistant.config import Configuration
from pi_assistant.main import get_keywords


def test_get_keywords_success():
    config = Configuration(environment="test")
    assert get_keywords(config) == [('noomis', 0.5)]
