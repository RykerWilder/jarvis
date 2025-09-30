from modules.voice import Voice
import urllib.request
import socket
import speedtest

#instances
voice = Voice()

class Network: 
    def check_connection(self):
        """
        Testing internet connection
        """
        try:
            urllib.request.urlopen("http://www.google.com", timeout=5)
            return True
        except (urllib.error.URLError, socket.timeout):
            return voice.text_to_speech("I don't have access to the internet.")

    def execute_speedtest(self):
        if check_connection():
            st = speedtest.Speedtest()
            
            # download
            download_speed = st.download() / 1_000_000  
            print(f"Download speed is {download_speed:.2f} Mbps")
            voice.text_to_speech(f"Download speed is {download_speed:.2f} Mbps")
            
            # upload
            upload_speed = st.upload() / 1_000_000 
            print(f"Upload speed is {upload_speed:.2f} Mbps")
            voice.text_to_speech(f"Upload speed is {upload_speed:.2f} Mbps")