# backend/app/services/llm_service.py
import requests
import json
from typing import Dict, Any
from ..utils.config import settings

class LLMService:
    def __init__(self):
        self.ollama_url = settings.OLLAMA_URL
        self.model = settings.LLM_MODEL  # "llama3" o "llama3:8b"

    def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Llama a Ollama localmente"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        except Exception as e:
            return f"Lo siento, en este momento no puedo procesar tu solicitud. Por favor, contacta a un asistente humano."

    def get_structured_response(self, system_prompt: str, user_message: str) -> Dict:
        """Obtiene respuesta estructurada (JSON)"""
        full_prompt = f"{system_prompt}\n\nUsuario: {user_message}\n\nRespuesta en formato JSON:"
        response = self.generate_response(full_prompt, temperature=0.3)
        try:
            return json.loads(response)
        except:
            return {"error": "No se pudo estructurar la respuesta"}
