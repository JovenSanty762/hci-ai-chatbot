from dotenv import load_dotenv
import os

load_dotenv()

# Configuración Ollama (IA del chatbot)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("LLM_MODEL", "llama3")

# Configuración general
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
