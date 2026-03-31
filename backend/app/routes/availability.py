from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Doctor, DoctorAvailability
from ..schemas.doctor import DoctorAvailabilityResponse

router = APIRouter(prefix="/doctors", tags=["Availability"])

@router.get("/{doctor_id}/availability", response_model=List[DoctorAvailabilityResponse])
def get_doctor_availability(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    # Verificar que el médico existe
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id, Doctor.is_active == True).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Médico no encontrado o inactivo")

    # Obtener todos los horarios configurados del médico
    availabilities = db.query(DoctorAvailability).filter(
        DoctorAvailability.doctor_id == doctor_id
    ).all()

    if not availabilities:
        # Si no tiene horarios configurados, devolvemos un mensaje claro
        raise HTTPException(
            status_code=404, 
            detail="Este médico no tiene horarios configurados todavía"
        )

    return availabilities
