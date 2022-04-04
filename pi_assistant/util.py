import os
from gtts import gTTS
from playsound import playsound


def assistant_reply(text: str) -> None:
    """
    A helper function which will convert a string text into an MP3 file which will be immediately played. The resulting
    text will be spoken via the assistant's voice. This is used by the plugins to reply to the user's command.
    :param: text: String the text to speak.
    :return: None
    """
    tts = gTTS(text=text, lang='en')
    tts.save('voice.mp3')
    playsound('voice.mp3')
    # Remove the file when
    os.unlink('voice.mp3')


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
