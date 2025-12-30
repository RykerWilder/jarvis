# Jarvis
is a voice assistant with built-in local AI that uses Ollama. You can modify variables in the .env file, such as SHUTDOWN_PHRASES to deactivate it, or, if you prefer to use a different Ollama model, you can modify OLLAMA_MODEL. 

## Installation
If you run Jarvis on MacOS you must have homebrew installed to download flac, portaudio, cmake and dlib.

1. Clone the repository
```bash
git clone https://github.com/RykerWilder/jarvis
```

2. Change directory
```bash
cd jarvis
```

3. Run the installer
```bash
bash installer.sh
```

4. Setup .env file

Now you are ready to use Jarvis, run `python3 main.py`.

**Jarvis uses face recognition to start. To register new face uncomment line 178 in modules/face_auth.py.**

## Tools

Jarvis already has some tools inside including: (* if you are connected to a network)

- Check internet connection
- Speedtest *
- Play music on youtube *
- Get current time
- Make a search on Google *
- Run terminal command
- Get weather information *