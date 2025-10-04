from langchain.agents import Tool

def get_tools(voice, net, time):
    """
    Returns the list of LangChain tools for the agent.
    
    Args:
        voice: Voice instance
        net: Network instance
        time: Time instance
    
    Returns:
        list: List of Tool objects
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
        )
    ]
    
    return tools