from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import speech_recognition as sr
import os
import pyttsx3

# Linux ALSA errors
os.environ['ALSA_PCM_CARD'] = '0'
os.environ['ALSA_PCM_DEVICE'] = '0'

load_dotenv()

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

    # get available voices and use the first one
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
    LLM = ChatOllama(model=os.getenv('OLLAMA_MODEL'), reasoning=False)
    system_prompt = "You are Jarvis, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always explain your reasoning simply when appropriate, and keep your responses conversational and concise."
    
    messages = [
        ("system", system_prompt),
        ("user", request)
    ]
    
    # response
    response = LLM.invoke(messages)
    print("AI:", response.content)
    return response.content

def jarvis_manager():

    while True:
        try:
            user_text = speech_recognizer()
            if user_text.lower() == os.getenv('TRIGGER_WORD').lower():
                text_to_speech("Hi Sir, how can i help you?")
                ollama_response = run_ollama(speech_recognizer())
                text_to_speech(ollama_response)
            elif user_text.lower() ==os.getenv('SHUTDOWN_WORD').lower():
                text_to_speech("Goodbye Sir.")
                break
        except KeyboardInterrupt:
            print("Jarvis interrupted.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    jarvis_manager()