# Create Python virtual environment
python -m venv venv

# Active Environment
.\venv\Scripts\Activate.ps1

# Install Command
pip install crewai pydantic python-dotenv pytest

# Start manually
ollama serve

# Ollama Installation
ollama pull llama3

# To run the model, use the command
ollama run llama3

# Check litning ports
netstat -ano | findstr 11434

# Kill ports
taskkill /PID 25036 /F
taskkill /IM ollama.exe /F