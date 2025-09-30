import urllib.request
import socket
import speedtest

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