# backend/app/routes/chatbot.py

import traceback
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from ..logger import logger
from ..services.llm_service import LLMService
from ..services.appointment_service import AppointmentService
from ..utils.conversation_manager import ConversationManager


router = APIRouter(prefix="/chatbot", tags=["chatbot"])

llm = LLMService()
conv_manager = ConversationManager()
appointment_service = AppointmentService()


class ChatMessage(BaseModel):
    conversation_id: str
    message: str
    patient_id: Optional[str] = None


@router.post("/message")
async def process_message(msg: ChatMessage):
    """
    Endpoint principal del chatbot.

    Flujo:
    1) Bienvenida
    2) Solicitud nombre y documento
    3) Selección de especialidad
    4) Confirmación
    5) Creación de cita
    6) Finalización automática
    """

    try:
        # Log inicial del request
        logger.info(
            f"[CHATBOT] Request recibido | conversation_id={msg.conversation_id} | "
            f"patient_id={msg.patient_id} | message='{msg.message}'"
        )

        # Validación básica
        if not msg.message or not msg.message.strip():
            logger.warning(f"[CHATBOT] Mensaje vacío recibido | conversation_id={msg.conversation_id}")
            return {
                "response": "Por favor escribe un mensaje para poder ayudarte.",
                "conversation_id": msg.conversation_id
            }

        user_message = msg.message.strip()

        # Guardar mensaje del usuario en historial
        conv_manager.save_message(msg.conversation_id, "user", user_message)

        # Obtener estado actual
        state = conv_manager.get_state(msg.conversation_id)

        if state is None:
            logger.warning(f"[CHATBOT] Estado nulo, creando estado inicial | conversation_id={msg.conversation_id}")
            state = {}

        step = state.get("step")

        logger.info(f"[CHATBOT] Estado actual | conversation_id={msg.conversation_id} | step={step}")

        # =========================================================
        # PASO 1: Bienvenida
        # =========================================================
        if step is None:
            welcome_prompt = """
Eres un asistente virtual del Hospital Central.
Tu función es ayudar a los pacientes a AGENDAR CITAS MÉDICAS.

Reglas:
- Responde siempre en español formal.
- Sé amable y profesional.
- NO realices diagnósticos médicos.
- NO recomiendes medicamentos.
- Solo guía al usuario para agendar citas.

Genera un mensaje de bienvenida institucional y solicita nombre completo y documento.
"""
            response = llm.generate_response(welcome_prompt)

            conv_manager.update_state(msg.conversation_id, {"step": "ask_name"})

            logger.info(f"[CHATBOT] Paso bienvenida ejecutado | conversation_id={msg.conversation_id}")

        # =========================================================
        # PASO 2: Extraer nombre y documento
        # =========================================================
        elif step == "ask_name":
            prompt = f"""
Extrae del siguiente mensaje el nombre completo y número de documento.

Mensaje del usuario: "{user_message}"

Responde SOLO en JSON válido con esta estructura:
{{
  "nombre": "Nombre completo",
  "documento": "Documento"
}}
"""

            try:
                data = llm.get_structured_response("", prompt)

                if not isinstance(data, dict):
                    logger.warning(
                        f"[CHATBOT] Respuesta no válida del LLM (no dict) | conversation_id={msg.conversation_id}"
                    )
                    data = {}

            except Exception as e:
                logger.error(
                    f"[CHATBOT] Error parseando JSON del LLM en ask_name | conversation_id={msg.conversation_id} | {str(e)}"
                )
                logger.error(traceback.format_exc())
                data = {}

            nombre = data.get("nombre")
            documento = data.get("documento")

            if not nombre or not documento:
                logger.warning(
                    f"[CHATBOT] No se pudo extraer nombre/documento | conversation_id={msg.conversation_id}"
                )
                response = (
                    "No pude identificar correctamente tu nombre y documento.\n\n"
                    "Por favor escríbelo en este formato:\n"
                    "Nombre: Juan Pérez\n"
                    "Documento: 123456789"
                )
                conv_manager.update_state(msg.conversation_id, {"step": "ask_name"})
            else:
                conv_manager.update_state(
                    msg.conversation_id,
                    {"step": "ask_specialty", "nombre": nombre, "documento": documento}
                )

                response = f"Gracias {nombre}. ¿Para qué especialidad deseas agendar la cita?"

                logger.info(
                    f"[CHATBOT] Datos extraídos correctamente | conversation_id={msg.conversation_id} | nombre={nombre}"
                )

        # =========================================================
        # PASO 3: Selección de especialidad
        # =========================================================
        elif step == "ask_specialty":
            specialties = appointment_service.get_specialties()

            prompt = f"""
El usuario dijo: "{user_message}"

Especialidades disponibles:
{specialties}

Devuelve SOLO JSON válido con esta estructura:
{{
  "especialidad": "Nombre exacto de la especialidad"
}}
"""

            try:
                data = llm.get_structured_response("", prompt)

                if not isinstance(data, dict):
                    logger.warning(
                        f"[CHATBOT] Respuesta no válida del LLM en ask_specialty | conversation_id={msg.conversation_id}"
                    )
                    data = {}

            except Exception as e:
                logger.error(
                    f"[CHATBOT] Error parseando JSON del LLM en ask_specialty | conversation_id={msg.conversation_id} | {str(e)}"
                )
                logger.error(traceback.format_exc())
                data = {}

            especialidad = data.get("especialidad")

            if not especialidad or especialidad not in specialties:
                logger.warning(
                    f"[CHATBOT] Especialidad inválida | conversation_id={msg.conversation_id} | especialidad={especialidad}"
                )
                response = (
                    "No reconocí esa especialidad.\n\n"
                    "Especialidades disponibles:\n- " + "\n- ".join(specialties) +
                    "\n\nPor favor escribe una de las opciones exactamente."
                )
                conv_manager.update_state(msg.conversation_id, {"step": "ask_specialty"})
            else:
                conv_manager.update_state(
                    msg.conversation_id,
                    {"step": "confirm", "especialidad": especialidad}
                )

                response = (
                    f"Perfecto. ¿Deseas agendar una cita en **{especialidad}**?\n"
                    "Responde con: SÍ o NO."
                )

                logger.info(
                    f"[CHATBOT] Especialidad seleccionada | conversation_id={msg.conversation_id} | especialidad={especialidad}"
                )

        # =========================================================
        # PASO 4: Confirmación
        # =========================================================
        elif step == "confirm":
            user_answer = user_message.strip().upper()

            if user_answer in ["SÍ", "SI", "YES"]:
                patient_id = msg.patient_id or "TEMP"
                especialidad = state.get("especialidad")

                if not especialidad:
                    logger.error(
                        f"[CHATBOT] Error: especialidad no encontrada en state | conversation_id={msg.conversation_id}"
                    )
                    conv_manager.update_state(msg.conversation_id, {"step": "ask_specialty"})
                    response = "Ocurrió un error con la especialidad. Por favor indícame nuevamente la especialidad."
                else:
                    appointment = appointment_service.create_appointment(
                        patient_id=patient_id,
                        specialty=especialidad,
                        conversation_id=msg.conversation_id
                    )

                    response = (
                        f"✅ Cita agendada exitosamente.\n\n"
                        f"📌 Especialidad: {especialidad}\n"
                        f"🧾 Número de cita: {appointment['id']}\n\n"
                        f"Gracias por usar el asistente virtual del Hospital Central.\n"
                        f"Si necesitas algo más, estaré disponible. ¡Feliz día!"
                    )

                    conv_manager.update_state(msg.conversation_id, {"step": "finished"})

                    logger.info(
                        f"[CHATBOT] Cita creada correctamente | conversation_id={msg.conversation_id} | appointment_id={appointment['id']}"
                    )

            elif user_answer in ["NO", "N"]:
                conv_manager.update_state(msg.conversation_id, {"step": "ask_specialty"})
                response = "Entendido. Por favor escribe la especialidad que deseas agendar."
                logger.info(f"[CHATBOT] Usuario rechazó confirmación | conversation_id={msg.conversation_id}")

            else:
                response = "Por favor responde únicamente con SÍ o NO."
                logger.warning(f"[CHATBOT] Respuesta inválida en confirmación | conversation_id={msg.conversation_id}")

        # =========================================================
        # PASO 5: Conversación finalizada
        # =========================================================
        elif step == "finished":
            response = (
                "La conversación ya fue finalizada ✅\n\n"
                "Si deseas agendar otra cita, por favor inicia una nueva conversación."
            )
            logger.info(f"[CHATBOT] Usuario escribió después de finalizar | conversation_id={msg.conversation_id}")

        # =========================================================
        # FALLBACK GENERAL
        # =========================================================
        else:
            logger.warning(
                f"[CHATBOT] Step desconocido, usando fallback | conversation_id={msg.conversation_id} | step={step}"
            )
            response = "Entendido. ¿Deseas agendar una cita médica? Indica la especialidad."

            conv_manager.update_state(msg.conversation_id, {"step": "ask_specialty"})

        # Guardar respuesta del bot
        conv_manager.save_message(msg.conversation_id, "assistant", response)

        logger.info(f"[CHATBOT] Respuesta enviada | conversation_id={msg.conversation_id}")

        return {"response": response, "conversation_id": msg.conversation_id}

    except Exception as e:
        logger.error(
            f"[CHATBOT] ERROR CRÍTICO | conversation_id={msg.conversation_id} | error={str(e)}"
        )
        logger.error(traceback.format_exc())

        return {
            "response": "⚠️ Ocurrió un error interno del servidor. Por favor intenta nuevamente.",
            "conversation_id": msg.conversation_id
        }
