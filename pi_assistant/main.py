import os
import socket
from wit import Wit
from gtts import gTTS
from pi_assistant.log import logger
from playsound import playsound
import speech_recognition as sr
from pi_assistant.config import Configuration
from pi_assistant.plugins.plugin_manager import PluginManager

config = Configuration()
recognizer = sr.Recognizer()
source = sr.Microphone()
plugin_manager = PluginManager(config=config)


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 65432))
        s.listen()
        logger.info(f"Initializing {len(plugin_manager.plugins)} plugins.")
        plugin_manager.init_plugins()
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


def get_keywords(config: Configuration):
    kw = config.get("voice_assistant.keywords")
    result = []
    for k in kw:
        result.append((k['text'], k['sensitivity']))
    return result


def assistant_reply(text: str):
    tts = gTTS(text=text, lang='en')
    tts.save('voice.mp3')
    playsound('voice.mp3')
    # Remove the file when
    os.unlink('voice.mp3')


# Called from the background thread
def callback(recognizer: sr.Recognizer, audio: sr.AudioData) -> None:
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


if __name__ == "__main__":
    run()
