

def sanitize_plugin_class_name(plugin_name: str) -> str:
    """
    Converts a non-standard plugin package name into its respective class name.
    :param: plugin_name: String a plugins name
    :return: The name of the class enclosed within the plugin package.
    """
    if plugin_name is None:
        return ""

    parts = plugin_name.split("_")

    sanitized = []
    for part in parts:
        part = part.capitalize()
        sanitized.append(part)
    sanitized.append("Plugin")
    return "".join(sanitized)