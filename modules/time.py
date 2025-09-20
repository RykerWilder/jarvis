import time
import threading
import sys
import os

def background_timer(seconds=0, minutes=0, hours=0):
    """
    Timer that runs in background (non-blocking).
    Returns the timer object so you can cancel it with timer.cancel()
    """
    total_time = hours * 3600 + minutes * 60 + seconds
    
    timer_obj = threading.Timer(total_time, play_beep_sound())
    timer_obj.start()
    return timer_obj

# Examples
if __name__ == "__main__":
    print("Starting 5-second timer...")
    # Background timer (doesn't block)
    bg_timer = background_timer(seconds=5)