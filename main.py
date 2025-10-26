import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType, Tool
# modules
from modules.voice import Voice
from modules.network import Network
from modules.time import Time
from modules.terminal import Terminal
from modules.tools import get_tools

# instances
voice = Voice()
net = Network()
time = Time()
term = Terminal()

# langchain tools
tools = get_tools(voice, net, time, term)

load_dotenv()

def load_system_prompt():
    with open('./system_prompt.txt', 'r') as f:
        return f.read().strip()

def run_ollama(request):
    # ollama configuration
    LLM = ChatOllama(model=os.getenv('OLLAMA_MODEL'), reasoning=False, temperature=0)
    
    # agent creation
    agent = initialize_agent(
        tools=tools,
        llm=LLM,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=3,
        return_intermediate_steps=False,
        early_stopping_method="generate"
    )

    SYSTEM_PROMPT = load_system_prompt()
    
    full_request = f"{SYSTEM_PROMPT}\n\nUser: {request}"
    
    response = agent.invoke({"input": full_request})
    
    final_output = response.get("output", "I couldn't process that request.")
    
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
    while True:
        try:
            user_text = voice.speech_recognizer()

            if user_text is None:
                voice.text_to_speech(f"I didn't understand {os.getenv("USER_TITLE")}. Please try again.")
                continue
            elif shutdown_command(user_text):
                voice.text_to_speech(f"Goodbye {os.getenv("USER_TITLE")}.")
                break
            elif os.getenv('TRIGGER_WORD').lower() in user_text.lower():
                ollama_response = run_ollama(user_text)
                voice.text_to_speech(ollama_response)
        
        except KeyboardInterrupt:
            voice.text_to_speech(f"Goodbye {os.getenv("USER_TITLE")}.")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    jarvis_manager()