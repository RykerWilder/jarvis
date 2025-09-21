import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

#modules
from modules.voice import Voice

# istances
voice = Voice()

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
    CONVERSATION_MODE = False

    voice.text_to_speech("Say the trigger word to activate.")
    user_text = voice.speech_recognizer()

    if user_text.lower() == os.getenv('TRIGGER_WORD').lower():
        CONVERSATION_MODE = True
        voice.text_to_speech("Hi Sir, how can i help you?")

    while CONVERSATION_MODE:
        try:
            user_text = voice.speech_recognizer()
            if user_text.lower() ==os.getenv('SHUTDOWN_WORD').lower():
                voice.text_to_speech("Goodbye Sir.")
                break
            else:
                ollama_response = run_ollama(voice.speech_recognizer())
                voice.text_to_speech(ollama_response)
        except KeyboardInterrupt:
            voice.text_to_speech("Goodbye Sir.")
            CONVERSATION_MODE = False
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    jarvis_manager()