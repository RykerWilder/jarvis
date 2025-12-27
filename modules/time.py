import time
import threading
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Time:
    def background_timer(self, seconds=0, minutes=0, hours=0):
        """
        Timer that runs in background (non-blocking).
        Returns the timer object so you can cancel it with timer.cancel()
        """
        total_time = hours * 3600 + minutes * 60 + seconds

        sound = Sound()
        
        timer_obj = threading.Timer(total_time, sound.play_beep_sound())
        timer_obj.start()
        return timer_obj

    def get_time(self, input_text=""):
        """
        Get current_time
        """
        current_time = datetime.now().strftime("%H:%M")
        return f"It's {current_time} {os.getenv("USER_TITLE")}."