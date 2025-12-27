import speech_recognition as sr
import pyttsx3


class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # get available voices
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "daniel" in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                break
        
        # parameters
        self.engine.setProperty('rate', 140)  # words speed
        self.engine.setProperty('volume', 0.9)  # volume (0.0 to 1.0)


    def speech_recognizer(self):
        # init
        r = sr.Recognizer()
        # microphone config
        with sr.Microphone(sample_rate=16000) as source:
            print("Listening...")
            # ambient noise
            r.adjust_for_ambient_noise(source, duration=2)
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.8         
            # listening
            audio = r.listen(source, timeout=10, phrase_time_limit=25)
        try:
            text = r.recognize_google(audio, language="en-US")
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None

    def text_to_speech(self, text):
        try:
            format_text = str(text)
            self.engine.say(format_text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
            self.engine = pyttsx3.init()
            self.engine.say(format_text)
            self.engine.runAndWait()

