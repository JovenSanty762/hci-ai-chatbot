from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from ..database import SessionLocal
from ..services.appointment_service import get_available_times, create_appointment
from ..utils.conversation_manager import init_conversation, get_state, update_state, end_conversation
from ..services.llm_service import ask_llama

router = APIRouter()

SPECIALTIES = [
    "Medicina General",
    "Pediatría",
    "Cardiología",
    "Dermatología",
    "Ginecología",
    "Ortopedia",
    "Neurología"
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    state = get_state(req.session_id)

    if not state:
        init_conversation(req.session_id)
        return {"response": "🏥 Bienvenido al asistente virtual del Hospital. ¿Qué especialidad deseas agendar?"}

    step = state["step"]
    msg = req.message.strip()

    # Paso: seleccionar especialidad
    if step == "welcome":
        if msg not in SPECIALTIES:
            return {"response": f"Especialidad no válida. Especialidades disponibles:\n- " + "\n- ".join(SPECIALTIES)}
        update_state(req.session_id, "date", "specialty", msg)
        return {"response": f"Perfecto. ¿Qué fecha deseas para {msg}? (Formato: YYYY-MM-DD)"}

    # Paso: fecha
    if step == "date":
        try:
            appointment_date = datetime.strptime(msg, "%Y-%m-%d").date()
        except:
            return {"response": "Formato incorrecto. Escribe la fecha como YYYY-MM-DD (Ej: 2026-04-01)"}

        update_state(req.session_id, "time", "appointment_date", str(appointment_date))

        specialty = state["data"]["specialty"]
        available_times = get_available_times(db, specialty, appointment_date)

        if not available_times:
            return {"response": "No hay horarios disponibles para esa fecha. Intenta con otra fecha."}

        times_text = "\n".join([t.strftime("%H:%M") for t in available_times])

        return {"response": f"Horarios disponibles:\n{times_text}\n\nEscribe el horario exacto (Ej: 09:00)"}

    # Paso: hora
    if step == "time":
        try:
            appointment_time = datetime.strptime(msg, "%H:%M").time()
        except:
            return {"response": "Hora inválida. Usa formato HH:MM (Ej: 09:00)"}

        update_state(req.session_id, "patient_name", "appointment_time", msg)
        return {"response": "Por favor escribe tu nombre completo:"}

    # Paso: nombre
    if step == "patient_name":
        update_state(req.session_id, "patient_document", "patient_name", msg)
        return {"response": "Ahora escribe tu número de documento:"}

    # Paso: documento y confirmación final
    if step == "patient_document":
        update_state(req.session_id, "confirm", "patient_document", msg)

        data = state["data"]

        specialty = data["specialty"]
        appointment_date = datetime.strptime(data["appointment_date"], "%Y-%m-%d").date()
        appointment_time = datetime.strptime(data["appointment_time"], "%H:%M").time()
        patient_name = data["patient_name"]
        patient_document = msg

        appointment = create_appointment(
            db,
            patient_name=patient_name,
            patient_document=patient_document,
            specialty=specialty,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        end_conversation(req.session_id)

        closing_message = (
            f"✅ Cita agendada exitosamente.\n\n"
            f"📌 Especialidad: {specialty}\n"
            f"📅 Fecha: {appointment_date}\n"
            f"🕒 Hora: {appointment_time.strftime('%H:%M')}\n"
            f"🧾 Radicado: {appointment.id}\n\n"
            f"Gracias por usar el asistente virtual del Hospital. ¡Feliz día!"
        )

        return {"response": closing_message}

    # fallback IA
    llm_prompt = f"""
Eres un asistente virtual hospitalario encargado únicamente de agendar citas médicas.
Responde en español formal y breve.
Usuario: {msg}
"""

    ai_response = ask_llama(llm_prompt)
    return {"response": ai_response}
