# backend/app/routes/chatbot.py
from fastapi import APIRouter
from pydantic import BaseModel
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

SYSTEM_PROMPT = """
Eres un asistente médico amable y profesional del Hospital Central (HCI).
Tu objetivo es ayudar al paciente a agendar una cita médica de forma natural y conversacional.

Reglas:
- Sé cálido, empático y claro.
- Pregunta la información necesaria (nombre, documento, teléfono, especialidad, fecha/hora preferida).
- Cuando tengas todos los datos necesarios, confirma con el paciente y agenda la cita.
- Al final de la cita siempre ofrece: "¿Deseas que un asistente humano revise tu solicitud?"
- Nunca inventes datos. Si falta información, pregúntala de forma natural.
- Responde siempre en español.

Mantén el contexto de toda la conversación.
"""

@router.post("/message")
async def process_message(msg: ChatMessage):
    # Guardar mensaje del usuario
    conv_manager.save_message(msg.conversation_id, "user", msg.message)

    # Obtener toda la historia
    history = conv_manager.get_history(msg.conversation_id)

    # Construir prompt completo para Ollama
    full_prompt = SYSTEM_PROMPT + "\n\n"
    for turn in history:
        full_prompt += f"{turn['role'].capitalize()}: {turn['content']}\n"

    full_prompt += "\nAsistente:"

    # Llamar a Ollama
    response = llm.generate_response(full_prompt, temperature=0.7)

    # Guardar respuesta del bot
    conv_manager.save_message(msg.conversation_id, "assistant", response)

    # Intentar detectar si el LLM ya quiere agendar (busca palabras clave o JSON)
    if any(word in response.lower() for word in ["agendada", "confirmada", "cita reservada"]):
        # Aquí puedes mejorar con JSON structured output en futuras versiones
        appointment_service.create_appointment_from_conversation(
            conversation_id=msg.conversation_id,
            patient_info=conv_manager.get_patient_info(msg.conversation_id)
        )

    return {
        "response": response,
        "conversation_id": msg.conversation_id
    }