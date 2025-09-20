import speech_recognition as sr
import pyttsx3
from langchain_ollama import ChatOllama
import os
import os
from dotenv import load_dotenv

load_dotenv()


# Linux ALSA errors
os.environ['ALSA_PCM_CARD'] = '0'
os.environ['ALSA_PCM_DEVICE'] = '0'

LLM = ChatOllama(model=os.getenv('OLLAMA_MODEL'), reasoning=False)

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
        return None
    except sr.RequestError as e:
        print(f"Error: {e}")
        return None

def text_to_speech(text):
    # init
    engine = pyttsx3.init()

    # Get available voices and use the first one
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
    
    # parameters
    engine.setProperty('rate', 130)    # words speed
    engine.setProperty('volume', 0.9)  # volume (0.0 to 1.0)
    format_text = str(text)
    engine.say(format_text)
    engine.runAndWait()
    engine.stop()  

def run_ollama(request):
    system_prompt = os.getenv('SYSTEM_PROMPT')
    
    messages = [
        ("system", system_prompt),
        ("user", request)
    ]
    
    # response
    response = LLM.invoke(messages)
    print("AI:", response.content)
    return response.content

if __name__ == "__main__":
    user_text = speech_recognizer()
    if user_text:
        ollama_response = run_ollama(user_text)
        text_to_speech(ollama_response)