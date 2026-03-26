from pydantic import BaseModel
from datetime import date, time

class AppointmentCreate(BaseModel):
    patient_name: str
    patient_document: str
    specialty: str
    appointment_date: date
    appointment_time: time

class AppointmentResponse(AppointmentCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
