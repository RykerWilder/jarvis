import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType, Tool
# modules
from modules.voice import Voice
from modules.network import Network
from modules.time import Time
from modules.tools import get_tools

# instances
voice = Voice()
net = Network()
time = Time()

# langchain tools
tools = get_tools(voice, net, time)

load_dotenv()

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
    
    # prompt
    system_prompt = """You are Jarvis, an intelligent, conversational AI assistant.
    Your goal is to be helpful, friendly, and informative. You can use available tools when needed to answer questions more accurately.

    Available tools:
    - SpeedTest: for testing internet speed and performance
    - ConnectionCheck: for checking internet connection status
    - PlayingMusic: for playing music on YouTube - use this when user asks to play music, songs, or videos
    - Search: for searching information on Google - use this when user asks to search or look up information
    - GetTime: for getting the current time and date - use this when user asks what time it is or the current date

    Always respond using only plain text without emoticons or emojis."""
    
    full_request = f"{system_prompt}\n\nUser: {request}"
    
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
    CONVERSATION_MODE = False
    voice.text_to_speech("Say the trigger word to activate.")
    user_text = voice.speech_recognizer()
    
    if user_text is None:
        voice.text_to_speech("I didn't hear anything.")
        return
    
    if user_text.lower() == os.getenv('TRIGGER_WORD').lower():
        CONVERSATION_MODE = True
        voice.text_to_speech(f"Hi {os.getenv(USER_TITLE)}, how can I help you?")
    elif shutdown_command(user_text):
        voice.text_to_speech(f"Goodbye {os.getenv(USER_TITLE)}.")
    else:
        voice.text_to_speech(f"Sorry {os.getenv(USER_TITLE)}, I didn't understand.")
    
    while CONVERSATION_MODE:
        try:
            user_text = voice.speech_recognizer()
            
            if user_text is None:
                voice.text_to_speech(f"I didn't hear well {os.getenv(USER_TITLE)}. Please try again.")
                continue
            
            if shutdown_command(user_text):
                voice.text_to_speech(f"Goodbye {os.getenv(USER_TITLE)}.")
                CONVERSATION_MODE = False
            else:
                ollama_response = run_ollama(user_text)
                voice.text_to_speech(ollama_response)
        
        except KeyboardInterrupt:
            voice.text_to_speech(f"Goodbye {os.getenv(USER_TITLE)}.")
            CONVERSATION_MODE = False
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    jarvis_manager()