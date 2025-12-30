#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    else
        OS="unknown"
    fi
}

# error handler
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# check homebrew on macOS
check_homebrew() {
    echo -e "${YELLOW}Checking Homebrew installation...${NC}"
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}Homebrew is not installed. Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || error_exit "Homebrew installation failed."
        
        # Add Homebrew to PATH for Apple Silicon Macs
        if [[ $(uname -m) == "arm64" ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        else
            echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/usr/local/bin/brew shellenv)"
        fi
        
        echo -e "${GREEN}Homebrew installed successfully!${NC}"
    else
        echo -e "${GREEN}Homebrew is already installed.${NC}"
    fi
}

# check dependencies
check_dependencies() {
    echo -e "${YELLOW}Checking dependencies...${NC}"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        if [[ "$OS" == "macos" ]]; then
            echo -e "${YELLOW}Git not found. Installing via Homebrew...${NC}"
            brew install git || error_exit "Git installation failed."
        else
            error_exit "Git is not installed. Please install it before proceeding."
        fi
    fi
    
    # Check Python3
    if ! command -v python3 &> /dev/null; then
        if [[ "$OS" == "macos" ]]; then
            echo -e "${YELLOW}Python3 not found. Installing via Homebrew...${NC}"
            brew install python@3 || error_exit "Python3 installation failed."
        else
            error_exit "Python3 is not installed. Please install it before proceeding."
        fi
    fi
    
    # Check python3-venv (only for Linux)
    if [[ "$OS" == "linux" ]]; then
        if ! python3 -c "import venv" &> /dev/null; then
            echo -e "${YELLOW}python3-venv not found. Installing...${NC}"
            sudo apt update && sudo apt install -y python3-venv python3-pip || error_exit "Failed to install python3-venv"
        fi
    fi
}

# python3 dependencies
install_python_deps() {
    echo -e "${YELLOW}Installing python3 dependencies...${NC}"
    
    # Create virtual environment
    python3 -m venv jarvis-venv || error_exit "Virtual environment creation failed."
    
    # Activate virtual environment
    source jarvis-venv/bin/activate || error_exit "Virtual environment activation failed."
    
    # Upgrade pip within the virtual environment
    python -m pip install --upgrade pip || error_exit "Pip upgrade failed."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        error_exit "requirements.txt not found in the repository."
    fi
    
    # Install requirements
    pip install -r requirements.txt || error_exit "Requirements installation failed."
}

# MAIN
main() {
    echo -e "${GREEN}Starting jarvis installation...${NC}"
    
    # Detect operating system
    detect_os
    
    # Check Homebrew if on macOS
    if [[ "$OS" == "macos" ]]; then
        check_homebrew
    fi
    
    check_dependencies
    install_python_deps
    
    echo -e "${GREEN}jarvis installed successfully!${NC}"
}

# Run main function only if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
