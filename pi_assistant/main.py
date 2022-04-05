import os
import socket
from wit import Wit
import speech_recognition as sr
from pi_assistant.log import logger
from pi_assistant.config import Configuration
from pi_assistant.util import assistant_reply
from pi_assistant.profile.Profile import Profile
from pi_assistant.plugins.plugin_manager import PluginManager

config = Configuration()
recognizer = sr.Recognizer()
source = sr.Microphone()
plugin_manager = PluginManager(config=config)


def start_assistant(profile: Profile) -> None:
    """
    Launches a server which initializes each plugin and registers a microphone in the background waiting for keywords
    so the assistant can reply!
    :return: None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 65432))
        s.listen()
        logger.info(f"Initializing plugins.")
        plugin_manager.init_plugins(profile)
        recognizer.listen_in_background(source, callback)
        logger.info("Listening for input keywords...")
        assistant_reply("I am ready to help!")
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


def get_keywords(c: Configuration) -> list:
    """
    Parses the keywords from the configuration into tuples where the first item
    is the keyword and the second item is its sensitivity.
    :param c: Application Configuration object
    :return: List of tuples.
    """
    kw = c.get("voice_assistant.keywords")
    result = []
    for k in kw:
        result.append((k['text'], k['sensitivity']))
    return result


# Called from the background thread
def callback(recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
    """
    A callback function registered with the SpeechRecognition Recognizer (for Sphinx). This callback executes each time
    vocal audio is detected.
    :param recognizer:
    :param audio:
    :return:
    """
    try:
        kw = config.get("voice_assistant.keywords")
        keywords = []
        for k in kw:
            keywords.append((k['text'], k['sensitivity']))
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)

        # Look for your "Ok Google" keyword in speech_as_text
        if "google" in speech_as_text or "hey google":
            logger.info(f"Found keyword in audio: \"{speech_as_text}\". Listening for primary directive.")
            if config.get("voice_assistant.reply_on_keyword_detection") is True:
                assistant_reply("im listening")
            recognize_main()

    except sr.UnknownValueError as e:
        pass
        # logger.debug(f"The word or phrase was not a recognized keyword. Recognized keywords are: {keywords}")


def recognize_main() -> None:
    """
    Function which is called once keywords specified in the application.yml are detected. This function uses google's
    speech recognition software to quickly process the users command and sends the command to Wit.ai for intent and
    entity analysis.

    Finally, this method invokes the plugin handler's handle_intent method to choose the correct plugin to handle the
    user's request.
    :return: None
    """
    logger.info("Listening for primary command...")
    audio = recognizer.listen(source)
    try:
        output = recognizer.recognize_google(audio_data=audio)
        logger.info(f"Sending command to Wit.ai: \"{output}\"")
        client = Wit(os.getenv("WIT_ACCESS_TOKEN"))
        res = client.message(output)

        if len(res['intents']) == 0:
            assistant_reply("Sorry I am not sure what you meant by that. Can you rephrase it?")
            return

        plugin_manager.handle_intent(res)
    except sr.UnknownValueError as e:
        logger.error(f"There was an error while attempting to transcribe the audio. Message = {str(e)}")
