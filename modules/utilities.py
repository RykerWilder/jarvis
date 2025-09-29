from voice import Voice
import speedtest

#instances
voice = Voice()

def execute_speedtest(): 
    st = speedtest.Speedtest()
    
    # download
    download_speed = st.download() / 1_000_000  
    print(f"La velocità in download è {download_speed:.2f} Mbps")
    voice.text_to_speech(f"La velocità in download è {download_speed:.2f} Mbps")
    
    # upload
    upload_speed = st.upload() / 1_000_000 
    print(f"La velocità in upload è {upload_speed:.2f} Mbps")
    voice.text_to_speech(f"La velocità in upload è {upload_speed:.2f} Mbps")