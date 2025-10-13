import subprocess
import platform
import os
import signal

class Terminal:
    #track processes
    def __init__(self):
        self.processes = []
    
    def detect_os(self):
        system = platform.system()
        if system == "Linux":
            return "linux"
        elif system == "Darwin":
            return "macos"
        elif system == "Windows":
            return "windows"
        else:
            return "unknown"
    
    def run(self, program):
        os_type = self.detect_os()
        try:
            if os_type == "linux":
                process = subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{program}; exec bash"])
                self.processes.append(process)
            elif os_type == "macos":
                applescript = f'tell application "Terminal" to activate\ntell application "Terminal" to do script "{program}"'
                process = subprocess.Popen(["osascript", "-e", applescript])
                self.processes.append(process)
            elif os_type == "windows":
                process = subprocess.Popen(f"start cmd /k {program}", shell=True)
                self.processes.append(process)
            else:
                return"Unsupported operating system."
        except Exception as e:
            return f"Error: {e}"