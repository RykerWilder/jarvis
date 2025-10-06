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
            r.adjust_for_ambient_noise(source, duration=2)

            r.energy_threshold = 400  
            r.dynamic_energy_threshold = True
            r.pause_threshold = 1.0

            # listening
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        try:
            text = r.recognize_google(audio, language="en-US")
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("I didn't understand.")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None

    def text_to_speech(self, text):
        # init
        engine = pyttsx3.init()

        # get available voices
        voices = engine.getProperty('voices')
        for voice in engine.getProperty("voices"):
            if "daniel" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break
        
        # parameters
        engine.setProperty('rate', 140)    # words speed
        engine.setProperty('volume', 0.9)  # volume (0.0 to 1.0)
        format_text = str(text)
        engine.say(format_text)
        engine.runAndWait()
        engine.stop()