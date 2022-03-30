from src.util import sanitize_plugin_class_name


def test_sanitize_plugin_class_name_success():
    assert sanitize_plugin_class_name("simple") == "SimplePlugin"


def test_sanitize_plugin_class_name_with_underscore():
    assert sanitize_plugin_class_name("more_complex_plugin") == "MoreComplexPluginPlugin"


def test_sanitize_plugin_class_name_with_null_value():
    assert sanitize_plugin_class_name(None) == ""
