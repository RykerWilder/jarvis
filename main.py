import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
# MODULES
from modules.voice import Voice
from modules.network import Network
from modules.time import Time
from modules.terminal import Terminal
from modules.tools import get_tools
from modules.face_auth import FaceAuthenticator


# INSTANCES
voice = Voice()
net = Network()
time = Time()
term = Terminal()
authenticator = FaceAuthenticator()


# LANGCHAIN TOOLS
tools = get_tools(voice, net, time, term)


load_dotenv()


def load_system_prompt():
    with open('./system_prompt.txt', 'r') as f:
        return f.read().strip()


def run_ollama(request):
    LLM = ChatOllama(model=os.getenv('OLLAMA_MODEL'), temperature=0)
    
    SYSTEM_PROMPT = load_system_prompt()
    
    agent = create_agent(
        model=LLM,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )

    response = agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })

    final_output = response["messages"][-1].content if response.get("messages") else "I couldn't process that request."
    
    print("Jarvis:", final_output)
    return final_output 


def shutdown_command(text):
    if not text:
        return False
    text = text.lower().strip()
    shutdown_phrases_str = os.getenv('SHUTDOWN_PHRASES', '')
    shutdown_phrases = [phrase.strip() for phrase in shutdown_phrases_str.split(',') if phrase.strip()]
    return any(phrase in text for phrase in shutdown_phrases)


def jarvis_manager():
    voice.text_to_speech("Starting face authentication...")
    
    if not authenticator.is_registered:
        print("No face registered. Starting registration...")
        if not authenticator.register_face(num_samples=5):
            print("Face registration failed. Exiting.")
            return
    
    if not authenticator.verify_face(tolerance=0.6):
        voice.text_to_speech("Authentication failed. Access denied.")
        return

    voice.text_to_speech(f"Welcome {os.getenv('USER_TITLE')}. I'm is ready.")
    
    while True:
        try:
            user_text = voice.speech_recognizer()
            
            if user_text is None:
                voice.text_to_speech(f"I didn't understand {os.getenv('USER_TITLE')}. Please try again.")
                continue
            
            if shutdown_command(user_text):
                voice.text_to_speech(f"Goodbye {os.getenv('USER_TITLE')}.")
                break
            
            try:
                ollama_response = run_ollama(user_text)
                if ollama_response and ollama_response.strip():
                    voice.text_to_speech(ollama_response)
                else:
                    voice.text_to_speech("I encountered an issue processing your request.")
            except Exception as agent_error:
                print(f"Agent error: {agent_error}")
                voice.text_to_speech("Sorry, I couldn't complete that task.")
                
        except KeyboardInterrupt:
            voice.text_to_speech(f"Goodbye {os.getenv('USER_TITLE')}.")
            break
        except Exception as e:
            print(f"Error: {e}")
            voice.text_to_speech("An error occurred. Please try again.")
            continue


if __name__ == "__main__":
    jarvis_manager()
