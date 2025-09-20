import speech_recognition as sr
import pyttsx3
import ollama
import os

# Linux ALSA errors
os.environ['ALSA_PCM_CARD'] = '0'
os.environ['ALSA_PCM_DEVICE'] = '0'

LLM = "deepseek-r1:1.5b"

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
            return text
            
        except sr.UnknownValueError:
            print("I didn't undestand.")
        except sr.RequestError as e:
            print(f"Error: {e}")

def text_to_speech(text): 
    # init
    engine = pyttsx3.init()

    # parameters
    engine.setProperty('rate', 150)        # words speed
    engine.setProperty('volume', 0.9)      # volume (0.0 to 1.0)
    engine.setProperty('voice', 'italian') # langauge

    format_text = str(text)
    engine.say(format_text)
    engine.runAndWait()

def run_ollama(request):

    prompt = [
        {
            'role': 'system', 
            'content': 'You are Jarvis, a voice assistant. Be polite and slightly humorous. End each response with "Sir".'
        },
        {
            'role': 'user', 
            'content': f' {request}'
        }
    ]

    # response
    response = ollama.chat(model=LLM, messages=prompt)
    print("AI:", response['message']['content'])

    return response['message']['content']


if __name__ == "__main__":
    user_text = speech_recognizer()
    ollama_response = run_ollama(user_text)
    text_to_speech(ollama_response)
    