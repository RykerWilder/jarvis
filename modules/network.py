import urllib.request
import socket
import os
import requests
import speedtest
import webbrowser
from dotenv import load_dotenv
from urllib.parse import quote_plus
import pywhatkit as kit
from voice import Voice

#instances
voice = Voice()

load_dotenv()

class Network: 
    def check_connection(self, input_text=""):
        """
        Testing internet connection
        """
        try:
            urllib.request.urlopen("http://www.google.com", timeout=5)
            return True
        except (urllib.error.URLError, socket.timeout):
            return False

    def execute_speedtest(self, input_text=""):
        """
        playing speedtest after check internet connection
        """
        if self.check_connection():
            voice.text_to_speech("Starting speedtest, please wait.")
            try: 
                st = speedtest.Speedtest()
                
                # download
                download_speed = st.download() / 1_000_000  
                
                # upload
                upload_speed = st.upload() / 1_000_000 

                result = f"Speed test completed. Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps."
                return result
            except Exception as e:
                return f"Error during speedtest {os.getenv("USER_TITLE")}."
        else:
            return f"I don't have access to the internet {os.getenv("USER_TITLE")}."

    def play_music(self, query):
        """
        Plays music on YouTube based on search query
        """
        if self.check_connection():
            try:
                kit.playonyt(query)
                return f"Playing {query} on YouTube {os.getenv("USER_TITLE")}."
            
            except Exception as e:
                return f"Error during playback: {str(e)}"
        else:
            return f"I don't have access to the internet {os.getenv("USER_TITLE")}."

    def search(self, query):
        """
        Execute a Google search
        """
        if self.check_connection:
            try:
                kit.search(query)
                return f"Search for '{query}' completed successfully {os.getenv("USER_TITLE")}."
            except Exception as e:
                return f"Search {query} failed {os.getenv("USER_TITLE")}."
        else:
            return f"I don't have access to the internet {os.getenv("USER_TITLE")}."

    def get_weather(self, location):
        if self.check_connection():
            try:
                url = f"https://www.meteo.it/?1&city={location}"
                webbrowser.open(url)
                
                return f"Weather search for '{location}' opened on meteo.it {os.getenv('USER_TITLE')}."
            except Exception as e:
                return f"It was not possible to access the weather in {location}, {os.getenv('USER_TITLE')}. Error: {str(e)}"
        else:
            return f"I don't have access to the internet {os.getenv('USER_TITLE')}."

if __name__ == "__main__":
    net = Network()
    net.get_weather("Rome")