import time
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
        print(speech_as_text)

        # Look for your "Ok Google" keyword in speech_as_text
        if "google" in speech_as_text or "hey google":
            recognize_main()

    except sr.UnknownValueError as e:
        print(f"Oops! Didn't catch that word or phrase. Error = {str(e)}")


def recognize_main():
    print("Recognizing Main phrase...")
    audio = r.listen(source)
    try:
        output = r.recognize_google(audio_data=audio)
        print(output)
    except sr.UnknownValueError as e:
        print(f"There was an error while attempting to transcribe the audio. Message = {str(e)}")


def start_recognizer():
    r.listen_in_background(source, callback)
    time.sleep(1000000)


if __name__ == "__main__":
    start_recognizer()
