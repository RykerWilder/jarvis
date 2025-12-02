import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.prompts import PromptTemplate
# MODULES
from modules.voice import Voice
from modules.network import Network
from modules.time import Time
from modules.terminal import Terminal
from modules.tools import get_tools

# INSTANCES
voice = Voice()
net = Network()
time = Time()
term = Terminal()

# LANGCHAIN TOOLS
tools = get_tools(voice, net, time, term)

load_dotenv()

def load_system_prompt():
    with open('./system_prompt.txt', 'r') as f:
        return f.read().strip()

def run_ollama(request):
    # OLLAMA CONFIG
    LLM = ChatOllama(model=os.getenv('OLLAMA_MODEL'), reasoning=False, temperature=0)
    
    SYSTEM_PROMPT = load_system_prompt()
    
    base_prompt = hub.pull("hwchase17/react")
    
    custom_prompt = PromptTemplate.from_template(
        f"{SYSTEM_PROMPT}\n\n" + base_prompt.template
    )
    
    agent = create_react_agent(
        llm=LLM,
        tools=tools,
        prompt=custom_prompt
    )
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=3,
        return_intermediate_steps=False
    )
    
    response = agent_executor.invoke({"input": request})
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
                voice.text_to_speech(f"I didn't understand {os.getenv('USER_TITLE')}. Please try again.")
                continue
            elif shutdown_command(user_text):
                voice.text_to_speech(f"Goodbye {os.getenv('USER_TITLE')}.")
                break
            elif os.getenv('TRIGGER_WORD').lower() in user_text.lower():
                ollama_response = run_ollama(user_text)
                voice.text_to_speech(ollama_response)
                
        except KeyboardInterrupt:
            voice.text_to_speech(f"Goodbye {os.getenv('USER_TITLE')}.")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    jarvis_manager()