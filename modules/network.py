import urllib.request
import socket
import requests
import speedtest
import webbrowser
from urllib.parse import quote_plus
import pywhatkit as kit
from modules.voice import Voice

#instances
voice = Voice()

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
            voice.text_to_speech("Starting speedtest, please attend.")
            st = speedtest.Speedtest()
            
            # download
            download_speed = st.download() / 1_000_000  
            
            # upload
            upload_speed = st.upload() / 1_000_000 

            result = f"Speed test completed. Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps"
            return result
        else:
            return "I don't have access to the internet."

    def play_music(self, query):
        """
        Plays music on YouTube based on search query
        """
        if self.check_connection():
            try:
                kit.playonyt(query)
                return f"Playing {query} on YouTube"
            
            except Exception as e:
                return f"Error during playback: {str(e)}"
        else:
            return "I don't have access to the internet."

    def search(self, query):
        """
        Execute a Google search
        """
        if self.check_connection:
            try:
                kit.search(query)
                return f"Search for '{query}' completed successfully"
            except Exception as e:
                return f"Search {query} failed."
        else:
            return "I don't have access to the internet."