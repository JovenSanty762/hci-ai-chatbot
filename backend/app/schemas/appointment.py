from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional
from ..models import AppointmentStatus

class AppointmentCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    appointment_date: date
    start_time: time
    end_time: time
    notes: Optional[str] = Field(None, max_length=500)

class AppointmentResponse(AppointmentCreate):
    id: int
    status: AppointmentStatus
    created_at: date

    class Config:
        from_attributes = True
