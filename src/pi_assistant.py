import os
import socket
from wit import Wit
from gtts import gTTS
from src.log import logger
from datetime import datetime
from playsound import playsound
import speech_recognition as sr
from src.config import Configuration
from src.plugins.plugin_manager import PluginManager


config = Configuration()
plugin_manager = PluginManager()
source = sr.Microphone()
r = sr.Recognizer()

def get_keywords():
    kw = config.get("voice_assistant.keywords")
    result = []
    for k in kw:
        print(k)
        result.append((k['text'], k['sensitivity']))
    return result


def speak(text: str):
    tts = gTTS(text=text, lang='en')
    tts.save('voice.mp3')
    playsound('voice.mp3')
    # Remove the file when
    os.unlink('voice.mp3')


# Called from the background thread
def callback(recognizer, audio):
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=get_keywords())

        # Look for your "Ok Google" keyword in speech_as_text
        if "google" in speech_as_text or "hey google":
            logger.info(f"Found keyword in audio: \"{speech_as_text}\". Listening for primary directive.")
            speak("im listening")
            recognize_main()

    except sr.UnknownValueError as e:
        pass
        # logger.debug(f"The word or phrase was not a recognized keyword. Recognized keywords are: {keywords}")


def recognize_main():
    logger.info("Listening for primary command...")
    audio = r.listen(source)
    try:
        output = r.recognize_google(audio_data=audio)
        logger.info(f"Sending command to Wit.ai: \"{output}\"")
        client = Wit(os.getenv("WIT_ACCESS_TOKEN"))
        res = client.message(output)
        print(res)
        # TODO possibly sort intents by confidence
        for intent in res['intents']:
            if intent['name'] == 'time':
                speak("The current time is " + datetime.now().strftime("%I:%M %p"))
                break
            if intent['name'] == 'date':
                now = datetime.now()
                suffix = 'th' if 11 <= now.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(now.day % 10, 'th')
                speak("The current date is " + now.strftime("%B {S}").replace('{S}', str(now.day) + suffix))
                break
    except sr.UnknownValueError as e:
        logger.error(f"There was an error while attempting to transcribe the audio. Message = {str(e)}")


def start_recognizer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 65432))
        s.listen()
        r.listen_in_background(source, callback)
        logger.info("Listening for input keywords...")
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


if __name__ == "__main__":
    start_recognizer()
