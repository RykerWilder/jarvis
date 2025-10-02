import urllib.request
import socket
import requests
import speedtest
import webbrowser
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

class Network: 
    def check_connection(self, input_text=""):
        """
        Testing internet connection
        """
        try:
            urllib.request.urlopen("http://www.google.com", timeout=5)
            return True
        except (urllib.error.URLError, socket.timeout):
            return "I don't have access to the internet."

    def execute_speedtest(self, input_text=""):
        if self.check_connection():
            st = speedtest.Speedtest()
            
            # download
            download_speed = st.download() / 1_000_000  
            
            # upload
            upload_speed = st.upload() / 1_000_000 

            result = f"Speed test completed. Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps"
            return result
        else:
            return "I don't have access to the internet."

    def play_music(self, song, artist):
        if self.check_connection():
            try:
                # query creation
                query = f"{song} {artist}"
                query_encoded = quote_plus(query)
                
                # URL
                search_url = f"https://www.youtube.com/results?search_query={query_encoded}"
                
                # request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(search_url, headers=headers)
                
                # looking for first result
                if 'watch?v=' in response.text:
                    start = response.text.find('watch?v=') + 8
                    video_id = response.text[start:start+11]
                    
                    # video URL
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    # open first result
                    webbrowser.open(video_url)
                    
                    return f"Playing {music} - {artist}"
                else:
                    return f"No results found for: {music} - {artist}"
            
            except Exception as e:
                return f"error during playback: {str(e)}"
        else:
            return "I don't have access to the internet."