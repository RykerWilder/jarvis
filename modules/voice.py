import speech_recognition as sr
import pyttsx3

class Voice:
    def speech_recognizer(self):

        # init
        r = sr.Recognizer()

        # microphone config
        with sr.Microphone() as source:
            print("Listening...")

            # ambient noise
            r.adjust_for_ambient_noise(source, duration=1)

            # listening
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        try:
            text = r.recognize_google(audio, language="it-IT")
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("I didn't undestand.")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None

    def text_to_speech(self, text):
        # init
        engine = pyttsx3.init()

        # get available voices and use the first one
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        
        # parameters
        engine.setProperty('rate', 130)    # words speed
        engine.setProperty('volume', 0.9)  # volume (0.0 to 1.0)
        format_text = str(self.text)
        engine.say(format_text)
        engine.runAndWait()
        engine.stop()  