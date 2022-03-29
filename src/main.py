import speech_recognition as sr
from speech_recognition import UnknownValueError


def run():
    print(sr.Microphone.list_microphone_names())
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source)
        print("Listening....")
        audio = r.listen(source)
        print("Analyzing audio....")
        try:
            output = r.recognize_google(audio_data=audio)
            print(output)
        except UnknownValueError as e:
            print(f"There was an error while attempting to transcribe the audio. Message = {str(e)}")

if __name__ == "__main__":
  run()
