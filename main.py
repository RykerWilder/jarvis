import speech_recognition as sr
import os

# Linux ALSA errors
os.environ['ALSA_PCM_CARD'] = '0'
os.environ['ALSA_PCM_DEVICE'] = '0'

def speech_recognizer():
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
            
        except sr.UnknownValueError:
            print("I didn't undestand.")
        except sr.RequestError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    speech_recognizer()