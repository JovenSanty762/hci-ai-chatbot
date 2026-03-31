from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional
from ..models import AppointmentStatus

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    start_time: time
    end_time: time
    notes: Optional[str] = None

class AppointmentResponse(AppointmentCreate):
    id: int
    status: AppointmentStatus
    created_at: date

    class Config:
        from_attributes = True
