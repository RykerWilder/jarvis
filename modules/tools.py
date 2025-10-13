from langchain.agents import Tool

def get_tools(voice, net, time, terminal):
    """
    Returns the list of LangChain tools for the agent.
    """
    tools = [
        Tool(
            name="SpeedTest",
            func=net.execute_speedtest,
            description="Useful for testing internet speed, measuring download/upload speed, and checking connection performance"
        ),
        Tool(
            name="ConnectionCheck",
            func=net.check_connection,
            description="Useful for checking internet connection status, verifying connectivity, and diagnosing network issues"
        ),
        Tool(
            name="PlayingMusic",
            func=net.play_music,
            description="Plays music on YouTube by searching for song name and artist. Use this when user asks to play, listen to, or put on a song. Automatically finds and plays the first matching result in the browser. Examples: 'play Bohemian Rhapsody by Queen', 'I want to listen to Imagine by John Lennon'."
        ),
        Tool(
            name="Search",
            func=net.search,
            description="Executes a Google search to find information on the web. Use this when user asks to search, look up, or find information about any topic. The function performs an internet search and displays the results. Examples: 'search for weather forecast', 'look up Python documentation', 'find best restaurants in Milan', 'search latest news about technology'."
        ),
        Tool(
            name="GetTime",
            func=time.get_time,
            description="Gets the current time. Use this when user asks what time it is or needs to know the current hour. Examples: 'what time is it?', 'tell me the time', 'what's the current time?'."
        ),
        Tool(
            name="RunTerminal",
            func=terminal.run,
            description="Executes a terminal command or program in a visible terminal window on the user's operating system. Works on Linux, macOS, and Windows. Use this when user asks to run a command, execute a program, or launch an application. The command will open in a new terminal window. Examples: 'run cmatrix', 'execute ls', 'launch python script.py', 'run npm start', 'execute git status'."
        ),
        Tool(
            name="GetWeather",
            func=net.get_weather,
            description="Gets weather information for a specific location by opening the Italian meteorological service (meteoam.it). Use this when user asks about weather, weather forecast, current conditions, or climate information for a location. The function opens the weather page in the browser. Examples: 'what's the weather in Milan?', 'check the weather for Rome', 'tell me the weather in Turin', 'get weather forecast for Naples'."
        ),
        Tool(
            name="StopProcess",
            func=terminal.stop_last_process,
            description="Stops and terminates the last process or command that was running in the terminal. Use this when the user wants to interrupt, kill, cancel, or stop a running program or command. The function will attempt a graceful termination first, and if that fails, it will force-kill the process. Examples: 'stop the current process', 'kill the running command', 'interrupt the program', 'stop execution', 'cancel the running script'."
        )
    ]
    return tools