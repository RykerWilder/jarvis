import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
# modules
from modules.voice import Voice

# instances
voice = Voice()
load_dotenv()

def run_ollama(request):
    LLM = ChatOllama(model=os.getenv('OLLAMA_MODEL'), reasoning=False)
    system_prompt = "You are Jarvis, an intelligent, conversational AI assistant. Your goal is to be helpful, friendly, and informative. You can respond in natural, human-like language and use tools when needed to answer questions more accurately. Always respond using only plain text without emoticons or emojis."   
    messages = [
        ("system", system_prompt),
        ("user", request)
    ]
    # response
    response = LLM.invoke(messages)
    print("Jarvis:", response.content)
    return response.content

def shutdown_command(text):
    if not text:
        return False
    
    text = text.lower().strip()
    
    shutdown_phrases_str = os.getenv('SHUTDOWN_PHRASES', '')
    shutdown_phrases = [phrase.strip() for phrase in shutdown_phrases_str.split(',') if phrase.strip()]
    return any(phrase in text for phrase in shutdown_phrases)

def jarvis_manager():
    CONVERSATION_MODE = False
    voice.text_to_speech("Say the trigger word to activate.")
    
    user_text = voice.speech_recognizer()
    if user_text is None:
        voice.text_to_speech("I didn't hear anything.")
        return
    
    if user_text.lower() == os.getenv('TRIGGER_WORD').lower():
        CONVERSATION_MODE = True
        voice.text_to_speech("Hi Sir, how can I help you?")
    elif shutdown_command(user_text):
        voice.text_to_speech("Goodbye Sir.")
    else:
        voice.text_to_speech("Sorry Sir, I didn't understand.")
    
    while CONVERSATION_MODE:
        try:
            user_text = voice.speech_recognizer()

            if user_text is None:
                voice.text_to_speech("I didn't hear anything. Please try again.")
                continue
            
            if shutdown_command(user_text):
                voice.text_to_speech("Goodbye Sir.")
                break
            else:
                ollama_response = run_ollama(user_text)
                voice.text_to_speech(ollama_response)
                
        except KeyboardInterrupt:
            voice.text_to_speech("Goodbye Sir.")
            CONVERSATION_MODE = False
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    jarvis_manager()