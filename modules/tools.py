from langchain_core.tools import tool


def get_tools(voice, net, time, terminal):
    """
    Returns the list of LangChain tools for the agent.
    """
    
    @tool
    def SpeedTest(input_text: str = "") -> str:
        """Useful for testing internet speed, measuring download/upload speed, and checking connection performance"""
        return net.execute_speedtest(input_text)
    
    @tool
    def ConnectionCheck(input_text: str = "") -> str:
        """Useful for checking internet connection status, verifying connectivity, and diagnosing network issues"""
        return net.check_connection(input_text)
    
    @tool
    def PlayingMusic(query: str) -> str:
        """Plays music on YouTube by searching for song name and artist. Use this when user asks to play, listen to, or put on a song. Automatically finds and plays the first matching result in the browser. Examples: 'play Bohemian Rhapsody by Queen', 'I want to listen to Imagine by John Lennon'."""
        return net.play_music(query)
    
    @tool
    def Search(query: str) -> str:
        """Executes a Google search to find information on the web. Use this when user asks to search, look up, or find information about any topic. The function performs an internet search and displays the results. Examples: 'search for weather forecast', 'look up Python documentation', 'find best restaurants in Milan', 'search latest news about technology'."""
        return net.search(query)
    
    @tool
    def GetTime(input_text: str = "") -> str:
        """Gets the current time. Use this when user asks what time it is or needs to know the current hour. Examples: 'what time is it?', 'tell me the time', 'what's the current time?'."""
        return time.get_time(input_text)
    
    @tool
    def RunTerminal(command: str) -> str:
        """Executes a terminal command or program in a visible terminal window on the user's operating system. Works on Linux, macOS, and Windows. Use this when user asks to run a command, execute a program, or launch an application. The command will open in a new terminal window. Examples: 'run cmatrix', 'execute ls', 'launch python script.py', 'run npm start', 'execute git status'."""
        return terminal.run(command)
    
    @tool
    def GetWeather(location: str) -> str:
        """Gets weather information for a specific location by opening the Italian meteorological service (meteoam.it). Use this when user asks about weather, weather forecast, current conditions, or climate information for a location. The function opens the weather page in the browser. Examples: 'what's the weather in Milan?', 'check the weather for Rome', 'tell me the weather in Turin', 'get weather forecast for Naples'."""
        return net.get_weather(location)
    
    return [
        SpeedTest,
        ConnectionCheck,
        PlayingMusic,
        Search,
        GetTime,
        RunTerminal,
        GetWeather
    ]
