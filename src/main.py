import time
from src.log import logger
import speech_recognition as sr

r = sr.Recognizer()

# Words that sphinx should listen closely for. 0-1 is the sensitivity
# of the wake word.
keywords = [("google", 1), ("hey google", 1),  ("ok google", 1)]

source = sr.Microphone()


# Called from the background thread
def callback(recognizer, audio):

    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        logger.info(speech_as_text)

        # Look for your "Ok Google" keyword in speech_as_text
        if "google" in speech_as_text or "hey google":
            recognize_main()

    except sr.UnknownValueError as e:
        logger.error(f"The word or phrase was not a recognized keyword. Recognized keywords are: {keywords}")


def recognize_main():
    logger.info("Listening for primary command...")
    audio = r.listen(source)
    try:
        output = r.recognize_google(audio_data=audio)
        logger.info(f"Sending command to Wit.ai: \"{output}\"")
    except sr.UnknownValueError as e:
        logger.error(f"There was an error while attempting to transcribe the audio. Message = {str(e)}")


def start_recognizer():
    logger.info("Listening for input keywords...")
    r.listen_in_background(source, callback)
    time.sleep(1000000)


if __name__ == "__main__":
    start_recognizer()
