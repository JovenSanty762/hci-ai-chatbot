# backend/app/services/appointment_service.py
from sqlalchemy.orm import Session
from ..models import Appointment, Specialty
from ..database import get_db
from datetime import datetime

class AppointmentService:
    def get_specialties(self):
        db = next(get_db())
        return [s.name for s in db.query(Specialty).all()]

    def create_appointment(self, patient_id: str, specialty: str, conversation_id: str):
        db = next(get_db())
        appointment = Appointment(
            patient_id=patient_id,
            specialty=specialty,
            status="pending",
            conversation_id=conversation_id,
            created_at=datetime.utcnow()
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return {"id": appointment.id, "status": "success"}
