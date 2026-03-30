# backend/app/services/appointment_service.py

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from ..database import SessionLocal
from ..models import Appointment
from ..logger import logger


class AppointmentService:
    """
    Servicio para manejo de citas médicas en MySQL.
    """

    def __init__(self):
        # Especialidades base (MVP)
        self.default_specialties = [
            "Medicina General",
            "Pediatría",
            "Cardiología",
            "Dermatología",
            "Ginecología",
            "Ortopedia",
            "Neurología"
        ]

    def get_specialties(self):
        """
        Retorna lista de especialidades disponibles.
        MVP: retorna lista fija.
        """
        logger.info("[AppointmentService] get_specialties ejecutado")
        return self.default_specialties

    def create_appointment(self, patient_id: str, specialty: str, conversation_id: str):
        """
        Crea una cita básica.
        MVP: no asigna fecha/hora todavía, solo registra solicitud.
        """

        if specialty not in self.default_specialties:
            logger.warning(f"[AppointmentService] Especialidad inválida: {specialty}")
            return {"id": None, "status": "error", "detail": "Especialidad inválida"}

        db = SessionLocal()

        try:
            appointment = Appointment(
                patient_name="TEMP",  # Se puede actualizar luego si tu modelo lo permite
                patient_document=patient_id,
                specialty=specialty,
                appointment_date=datetime.utcnow().date(),
                appointment_time=datetime.utcnow().time(),
                status="scheduled",
                created_at=datetime.utcnow()
            )

            db.add(appointment)
            db.commit()
            db.refresh(appointment)

            logger.info(
                f"[AppointmentService] Cita creada | id={appointment.id} | specialty={specialty} | conversation_id={conversation_id}"
            )

            return {"id": appointment.id, "status": "success"}

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"[AppointmentService] Error SQLAlchemy creando cita: {str(e)}")
            return {"id": None, "status": "error", "detail": "Error en base de datos"}

        except Exception as e:
            db.rollback()
            logger.error(f"[AppointmentService] Error inesperado creando cita: {str(e)}")
            return {"id": None, "status": "error", "detail": "Error interno"}

        finally:
            db.close()
