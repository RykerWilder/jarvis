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
                # Prova gnome-terminal, altrimenti xterm
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{program}; exec bash"])
                # Alternativa: subprocess.Popen(["xterm", "-hold", "-e", program])
                
            elif os_type == "macos":
                # Apre Terminal.app e esegue il comando
                applescript = f'tell application "Terminal" to activate\ntell application "Terminal" to do script "{program}"'
                subprocess.Popen(["osascript", "-e", applescript])
                
            elif os_type == "windows":
                # /k mantiene la finestra aperta dopo l'esecuzione
                subprocess.Popen(f"start cmd /k {program}", shell=True)
                
            else:
                print("Unsupported operating system.")
        except Exception as e:
            print(f"Errore nell'esecuzione: {e}")