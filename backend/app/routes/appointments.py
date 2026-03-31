from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import Appointment, Doctor, Patient, DoctorAvailability
from ..schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    
    # 1. Verificar que el paciente existe
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # 2. Verificar que el médico existe y está activo
    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id, 
        Doctor.is_active == True
    ).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico no encontrado o inactivo")

    # 3. Validar que la hora de fin sea mayor que la hora de inicio
    if appointment.end_time <= appointment.start_time:
        raise HTTPException(status_code=400, detail="La hora de fin debe ser mayor que la hora de inicio")

    # 4. (Opcional pero recomendado) Verificar que el médico tenga disponibilidad ese día y horario
    # Aquí puedes agregar lógica más avanzada de verificación de solapamientos

    # 5. Crear la cita
    db_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        notes=appointment.notes,
        status=AppointmentStatus.PENDIENTE
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment
