# backend/app/services/llm_service.py

import requests
import json
import re
from typing import Dict, Any
from ..config import OLLAMA_URL, OLLAMA_MODEL
from ..logger import logger
from ..utils.config import settings


class LLMService:
    """
    Servicio de conexión con Ollama + Llama3 (local).
    """

    def __init__(self):
        self.ollama_url = OLLAMA_URL
        self.model = OLLAMA_MODEL

        logger.info(f"[LLMService] Inicializado | model={self.model} | url={self.ollama_url}")

    def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
#       payload = {
#           "model": self.model,
#            "prompt": prompt,
#            "stream": False,
#            "options": {
#                "temperature": temperature
#            }
#        }
#
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=90
            )
            response.raise_for_status()
            logger.info("[LLMService] Respuesta exitosa desde Ollama")
            llm_response = response.json().get("response", "").strip()
            return llm_response if llm_response else "⚠️ El modelo IA no devolvió respuesta."

        except requests.exceptions.Timeout:
            logger.error("[LLMService] Timeout conectando con Ollama")
            return "⚠️ El motor IA tardó demasiado en responder. Intenta nuevamente."

        except requests.exceptions.ConnectionError:
            logger.error("[LLMService] Error de conexión con Ollama (ConnectionError)")
            return "⚠️ No se pudo conectar con el motor IA. Verifica que Ollama esté activo."

        except requests.exceptions.RequestException as e:
            logger.error(f"[LLMService] Error RequestException: {str(e)}")
            return "⚠️ Error al comunicarse con el motor IA."

        except Exception as e:
            logger.error(f"[LLMService] Error inesperado: {str(e)}")
            return "⚠️ Error inesperado en el motor IA."

    def _extract_json(self, text: str) -> str:
        """
        Intenta extraer el primer bloque JSON válido dentro del texto.
        Ollama/LLMs a veces devuelven texto antes o después del JSON.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0)
        return ""

    def get_structured_response(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """
        Obtiene una respuesta estructurada tipo JSON.
        Si falla el parseo, devuelve un dict con error.
        """

        full_prompt = f"""
{system_prompt}

Usuario: {user_message}

IMPORTANTE:
- Responde únicamente en JSON válido.
- No incluyas texto adicional fuera del JSON.
"""

        raw_response = self.generate_response(full_prompt, temperature=0.2)

        if not raw_response:
            logger.warning("[LLMService] Respuesta vacía en structured_response")
            return {"error": "empty_response"}

        try:
            return json.loads(raw_response)

        except json.JSONDecodeError:
            logger.warning("[LLMService] JSON inválido recibido, intentando extracción...")
            extracted = self._extract_json(raw_response)

            if not extracted:
                logger.error(f"[LLMService] No se encontró JSON en respuesta: {raw_response}")
                return {"error": "invalid_json", "raw": raw_response}

            try:
                return json.loads(extracted)
            except Exception as e:
                logger.error(f"[LLMService] Falló parseo JSON extraído: {str(e)}")
                return {"error": "invalid_json_extracted", "raw": raw_response}

        except Exception as e:
            logger.error(f"[LLMService] Error inesperado parseando JSON: {str(e)}")
            return {"error": "unexpected_error", "raw": raw_response}
