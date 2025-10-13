import subprocess
import platform

class Terminal:
    def detect_os(self):
        """Rileva il sistema operativo"""
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
        """Esegue un programma nel terminale in base all'OS"""
        os_type = self.detect_os()  # IMPORTANTE: Chiama il metodo con ()
        
        if os_type == "linux":
            subprocess.Popen(["xterm", "-e", program])
        elif os_type == "macos":
            applescript = f'tell application "Terminal" to do script "{program}"'
            subprocess.Popen(["osascript", "-e", applescript])
        elif os_type == "windows":
            subprocess.Popen(f"start cmd /k {program}", shell=True)
        else:
            return "Unsupported operating system."

# Esempio di utilizzo
if __name__ == "__main__":
    terminal = Terminal()
    terminal.run("cmatrix")