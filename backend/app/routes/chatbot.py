# backend/app/routes/chatbot.py
import traceback
from fastapi import APIRouter, Depends
from pydantic import BaseModel
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
    patient_id: str = None

@router.post("/message")
async def process_message(msg: ChatMessage):
    # Guardar mensaje entrante
    conv_manager.save_message(msg.conversation_id, "user", msg.message)

    state = conv_manager.get_state(msg.conversation_id)

    # === FLUJO DEL CHATBOT ===
    if state.get("step") is None:
        # Mensaje de bienvenida
        welcome_prompt = """Eres un asistente médico amable del Hospital Central. 
        Saluda al paciente, explícale que eres un chatbot con IA y que vas a ayudarlo a agendar una cita.
        Sé cálido y profesional."""
        response = llm.generate_response(welcome_prompt)
        conv_manager.update_state(msg.conversation_id, {"step": "ask_name"})

    elif state.get("step") == "ask_name":
        # Extraer nombre y documento
        prompt = f"""Extrae del siguiente mensaje: nombre completo y número de documento.
        Mensaje: {msg.message}
        Responde SOLO en JSON: {{"nombre": "...", "documento": "..."}}"""
        data = llm.get_structured_response("", prompt)
        conv_manager.update_state(msg.conversation_id, {"step": "ask_specialty", **data})
        response = f"Gracias {data.get('nombre', 'paciente')}. ¿Para qué especialidad deseas agendar la cita?"

    elif state.get("step") == "ask_specialty":
        specialties = appointment_service.get_specialties()
        prompt = f"""El usuario dijo: {msg.message}
        Especialidades disponibles: {specialties}
        Devuelve JSON: {{"especialidad": "nombre exacto de la especialidad"}}"""
        data = llm.get_structured_response("", prompt)
        conv_manager.update_state(msg.conversation_id, {"step": "confirm", "especialidad": data.get("especialidad")})
        response = f"Perfecto. ¿Deseas agendar en {data.get('especialidad')}? Confirma con 'SÍ'."

    elif state.get("step") == "confirm" and msg.message.upper() in ["SÍ", "SI", "YES"]:
        # Crear cita
        appointment = appointment_service.create_appointment(
            patient_id=msg.patient_id or "TEMP",
            specialty=state["especialidad"],
            conversation_id=msg.conversation_id
        )
        response = f"✅ Cita agendada exitosamente. Número de cita: {appointment['id']}\n\nGracias por usar nuestro servicio. ¿Deseas que un asistente humano revise tu solicitud?"
        conv_manager.update_state(msg.conversation_id, {"step": "finished"})
    else:
        response = "Entendido. ¿En qué más puedo ayudarte?"

    # Guardar respuesta del bot
    conv_manager.save_message(msg.conversation_id, "assistant", response)

    return {"response": response, "conversation_id": msg.conversation_id}
