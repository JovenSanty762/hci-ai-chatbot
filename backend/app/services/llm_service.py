import requests
from ..config import OLLAMA_URL, OLLAMA_MODEL

def ask_llama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    return data.get("response", "No se obtuvo respuesta del modelo IA.")
