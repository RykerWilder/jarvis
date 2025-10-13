import subprocess
import platform
import os

class Terminal:
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
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{program}; exec bash"])
                
            elif os_type == "macos":
                applescript = f'tell application "Terminal" to activate\ntell application "Terminal" to do script "{program}"'
                subprocess.Popen(["osascript", "-e", applescript])
                
            elif os_type == "windows":
                subprocess.Popen(f"start cmd /k {program}", shell=True)
                
            else:
                return "Unsupported operating system."
        except Exception as e:
            return f"Errore nell'esecuzione: {e}"