# backend/app/services/llm_service.py
import requests
import json
from typing import Dict, Any
from ..utils.config import settings
from ..config import OLLAMA_URL, OLLAMA_MODEL
from ..logger import logger

class LLMService:
    def __init__(self):
        self.ollama_url = settings.OLLAMA_URL
        self.model = settings.LLM_MODEL  # "llama3" o "llama3:8b"

    def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
        payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            logger.info("Respuesta exitosa desde Ollama/Llama3")
            return data.get("response", "No se obtuvo respuesta del modelo IA.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error conectando con Ollama: {str(e)}")
            return "⚠️ No es posible conectarse al motor IA en este momento. Intenta más tarde."

    def get_structured_response(self, system_prompt: str, user_message: str) -> Dict:
        """Obtiene respuesta estructurada (JSON)"""
        full_prompt = f"{system_prompt}\n\nUsuario: {user_message}\n\nRespuesta en formato JSON:"
        response = self.generate_response(full_prompt, temperature=0.3)
        try:
            return json.loads(response)
        except:
            return {"error": "No se pudo estructurar la respuesta"}
