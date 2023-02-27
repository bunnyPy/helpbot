import speech_recognition as sr
from gtts import gTTS
import playsound
import sys
import time
import openai
import datetime

openai.api_key = "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"


def audio_file_name():
    current_time = datetime.datetime.now()
    filename = "./audio/audio-{}.mp3".format(current_time.strftime("%Y-%m-%d_%H-%M-%S"))
    filename = filename.replace(":", "_")  # replace colon with underscore
    return filename


def openai_response(text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.6,
        max_tokens=1000,
    )
    return response.choices[0].text


class SpeechToText:
    def __init__(self, language):
        self.language = language

    def convert(self):
        # Creating a recognizer object
        r = sr.Recognizer()

        # Using the microphone as a source
        with sr.Microphone() as source:
            print("Speak something...")
            # Adjusting the recognizer's sensitivity to ambient noise
            r.adjust_for_ambient_noise(source)
            # Listening for audio input
            audio = r.listen(source)

        try:
            print("Converting speech to text...")
            # Using the Google Web Speech API to recognize the audio input
            text = r.recognize_google(audio, language=self.language)
            print(f"You said: {text}")
            if text == "close":
                sys.exit(0)
            text = openai_response(text)
            print(f"OpenAI return: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API: {e}")
        return None


class TextToSpeech:
    def __init__(self, text, language, name):
        self.text = text
        self.language = language
        self.name = name

    def convert(self):
        # Passing the text and language to the engine
        tts = gTTS(text=self.text, lang=self.language)

        # Saving the converted audio to a file named hello.mp3
        tts.save(self.name)

        # Playing the converted audio
        playsound.playsound(self.name)

        time.sleep(2)


def main():
    # Language in which you want to convert the speech
    language1 = 'en-US'
    # Language in which you want to convert the text
    language2 = 'fr'

    while True:
        # Creating an instance of SpeechToText class and calling its convert method
        stt = SpeechToText(language1)
        text = stt.convert()

        if text is not None:
            # create audio file name with timestamp
            audio_file = audio_file_name()
            # Creating an instance of TextToSpeech class and calling its convert method
            tts = TextToSpeech(text, language1, audio_file)
            tts.convert()


if __name__ == '__main__':
    main()
