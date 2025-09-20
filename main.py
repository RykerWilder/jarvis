from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os


# Linux ALSA errors
os.environ['ALSA_PCM_CARD'] = '0'
os.environ['ALSA_PCM_DEVICE'] = '0'

load_dotenv()

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