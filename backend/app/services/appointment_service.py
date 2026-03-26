from sqlalchemy.orm import Session
from datetime import time
from ..models import Appointment

AVAILABLE_TIMES = [
    time(8, 0),
    time(9, 0),
    time(10, 0),
    time(11, 0),
    time(14, 0),
    time(15, 0),
    time(16, 0)
]

def get_available_times(db: Session, specialty: str, appointment_date):
    booked_times = db.query(Appointment.appointment_time).filter(
        Appointment.specialty == specialty,
        Appointment.appointment_date == appointment_date,
        Appointment.status == "scheduled"
    ).all()

    booked_times = [t[0] for t in booked_times]

    return [t for t in AVAILABLE_TIMES if t not in booked_times]

def create_appointment(db: Session, patient_name, patient_document, specialty, appointment_date, appointment_time):
    appointment = Appointment(
        patient_name=patient_name,
        patient_document=patient_document,
        specialty=specialty,
        appointment_date=appointment_date,
        appointment_time=appointment_time
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
