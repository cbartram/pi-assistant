

def sanitize_plugin_class_name(plugin_name: str, config: bool = False) -> str:
    """
    Converts a non-standard plugin package name into its respective class name.
    :param: plugin_name: String a plugins name
    :param: config: Boolean true if it should convert into a config name instead of a class name. For given package:
    philips_hue_lights when config is false it will produce PhilipsHueLightsPlugin and when its true it will produce
    PhilipsHueLightsConfig
    :return: The name of the class enclosed within the plugin package.
    """
    if plugin_name is None:
        return ""

    parts = plugin_name.split("_")

    sanitized = []
    for part in parts:
        part = part.capitalize()
        sanitized.append(part)
    sanitized.append("Plugin" if not config else "Config")
    return "".join(sanitized)
