# Jarvis
is a voice assistant with built-in local AI that uses Ollama. You can modify variables in the .env file, such as TRIGGER_WORD to activate Jarvis, SHUTDOWN_WORD to deactivate it, or, if you prefer to use a different Ollama model, you can modify OLLAMA_MODEL.

## Installation
If you run Jarvis on MacOS you probably need to install also flac and portaudio.
To install Jarvis, you can copy and paste the command into the terminal.

```bash
wget https://raw.githubusercontent.com/rykerwilder/jarvis/main/installer.sh
```

**Run the installer**

```bash
bash ./installer.sh
```

After running the installer, follow the instructions in your terminal to activate Jarvis.

## Tools

Jarvis already has some tools inside including:

- Check internet connection
- Speedtest (if you are connected to a network)
- Play music on youtube (if you are connected to a network)
- Get current time
- Make a search on Google (if you are connected to a network)